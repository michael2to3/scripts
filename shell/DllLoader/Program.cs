using System;
using System.Reflection;

class DllLoader
{
    static void Main(string[] args)
    {
        if (args.Length == 0)
        {
            Console.WriteLine("Usage: DllLoader <path_to_dll>");
            return;
        }

        string dllPath = args[0];

        try
        {
            Assembly assembly = Assembly.LoadFrom(dllPath);
            Console.WriteLine($"DLL {dllPath} loaded successfully.");

            Type[] types = assembly.GetTypes();
            Console.WriteLine("Available types in the DLL:");

            foreach (Type type in types)
            {
                Console.WriteLine(type.FullName);

                try
                {
                    Activator.CreateInstance(type);
                    Console.WriteLine($"Instance of {type.FullName} created.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error creating instance of {type.FullName}: {ex.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error loading or handling DLL: {ex.Message}");
        }

        Console.WriteLine("Program finished.");
    }
}
