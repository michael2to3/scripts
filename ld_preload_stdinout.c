// gcc -shared -fPIC -o ld_preload_stdinout.so ld_preload_stdinout.c -ldl
#define _GNU_SOURCE
#include <dlfcn.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

static ssize_t (*real_write)(int fd, const void *buf, size_t count) = NULL;
static ssize_t (*real_read)(int fd, void *buf, size_t count) = NULL;
static int (*real_printf)(const char *format, ...) = NULL;
static int (*real_puts)(const char *s) = NULL;
static int (*real_fprintf)(FILE *stream, const char *format, ...) = NULL;

static int log_fd = -1;

__attribute__((constructor)) void my_init(void) {
  real_write = dlsym(RTLD_NEXT, "write");
  real_read = dlsym(RTLD_NEXT, "read");
  real_printf = dlsym(RTLD_NEXT, "printf");
  real_puts = dlsym(RTLD_NEXT, "puts");
  real_fprintf = dlsym(RTLD_NEXT, "fprintf");

  log_fd = open("/tmp/file.log", O_WRONLY | O_CREAT | O_APPEND, 0666);
  if (log_fd == -1) {
    perror("Failed to open log file");
    exit(1);
  }

  setbuf(stdout, NULL);
  setbuf(stderr, NULL);
}

__attribute__((destructor)) void my_fini(void) {
  if (log_fd != -1) {
    close(log_fd);
  }
}

ssize_t write(int fd, const void *buf, size_t count) {
  ssize_t result = real_write(fd, buf, count);

  if ((fd == STDOUT_FILENO || fd == STDERR_FILENO) && fd != log_fd) {
    real_write(log_fd, buf, count);
  }

  return result;
}

ssize_t read(int fd, void *buf, size_t count) {
  ssize_t result = real_read(fd, buf, count);

  if (fd == STDIN_FILENO && fd != log_fd) {
    real_write(log_fd, buf, result);
  }

  return result;
}

int printf(const char *format, ...) {
  va_list args;
  va_start(args, format);
  int result = vfprintf(stdout, format, args);
  va_end(args);

  va_start(args, format);
  real_fprintf(log_fd != -1 ? fdopen(log_fd, "w") : stderr, format, args);
  va_end(args);

  return result;
}

int puts(const char *s) {
  int result = real_puts(s);

  if (log_fd != -1) {
    real_write(log_fd, s, strlen(s));
    real_write(log_fd, "\n", 1);
  }

  return result;
}

int fprintf(FILE *stream, const char *format, ...) {
  va_list args;
  va_start(args, format);
  int result = real_fprintf(stream, format, args);
  va_end(args);

  if (stream == stdout || stream == stderr) {
    va_start(args, format);
    real_fprintf(log_fd != -1 ? fdopen(log_fd, "w") : stream, format, args);
    va_end(args);
  }

  return result;
}
