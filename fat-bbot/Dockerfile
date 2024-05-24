FROM blacklanternsecurity/bbot:dev

COPY ./gitconfig /root/.gitconfig
RUN pip install baddns badsecrets
RUN bbot --install-all-deps
