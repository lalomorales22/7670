import java.util.*;
import javax.script.ScriptEngineManager;
import javax.script.ScriptEngine;
import javax.script.ScriptException;

public class JavaLearningProgram {
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("Welcome to the Comprehensive Java Learning Program!");
        
        while (true) {
            System.out.println("\nChoose a topic to learn about:");
            System.out.println("1. Basic Syntax and Structure");
            System.out.println("2. Variables and Data Types");
            System.out.println("3. Operators");
            System.out.println("4. Control Flow");
            System.out.println("5. Arrays and Collections");
            System.out.println("6. Object-Oriented Programming Basics");
            System.out.println("7. Exception Handling");
            System.out.println("8. File I/O");
            System.out.println("9. Exit");
            
            int choice = getIntInput("Enter your choice (1-9): ");
            
            switch (choice) {
                case 1:
                    learnBasicSyntax();
                    break;
                case 2:
                    learnVariablesAndDataTypes();
                    break;
                case 3:
                    learnOperators();
                    break;
                case 4:
                    learnControlFlow();
                    break;
                case 5:
                    learnArraysAndCollections();
                    break;
                case 6:
                    learnOOPBasics();
                    break;
                case 7:
                    learnExceptionHandling();
                    break;
                case 8:
                    learnFileIO();
                    break;
                case 9:
                    System.out.println("Thank you for using the Java Learning Program. Goodbye!");
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    private static void learnBasicSyntax() {
        System.out.println("\n--- Basic Syntax and Structure ---");
        System.out.println("Java programs are composed of classes and methods. Here's a basic structure:");
        
        String basicStructure = 
            "public class MyClass {\n" +
            "    public static void main(String[] args) {\n" +
            "        // Your code here\n" +
            "        System.out.println(\"Hello, World!\");\n" +
            "    }\n" +
            "}";
        
        System.out.println(basicStructure);
        
        System.out.println("\nKey points:");
        System.out.println("1. Class names should start with a capital letter.");
        System.out.println("2. The main method is the entry point of your program.");
        System.out.println("3. Java statements end with a semicolon (;).");
        System.out.println("4. Code blocks are enclosed in curly braces {}.");
        
        System.out.println("\nLet's practice! Write a simple Java program that prints your name:");
        String userProgram = getUserMultiLineInput();
        
        System.out.println("\nGreat! Here's how your program might look if formatted:");
        System.out.println(formatJavaCode(userProgram));
    }

    private static void learnVariablesAndDataTypes() {
        System.out.println("\n--- Variables and Data Types ---");
        System.out.println("Java has two categories of data types:");
        System.out.println("1. Primitive Types: byte, short, int, long, float, double, boolean, char");
        System.out.println("2. Reference Types: String, Arrays, Classes, Interfaces");
        
        System.out.println("\nVariable Declaration and Initialization:");
        System.out.println("dataType variableName = value;");
        
        System.out.println("\nExamples:");
        System.out.println("int age = 25;");
        System.out.println("double price = 19.99;");
        System.out.println("String name = \"John\";");
        
        System.out.println("\nLet's practice! Declare and initialize variables for:");
        System.out.println("1. Your age (int)");
        System.out.println("2. Your height in meters (double)");
        System.out.println("3. Your name (String)");
        
        String userVariables = getUserMultiLineInput();
        System.out.println("\nGreat! Here's how your variables look:");
        System.out.println(formatJavaCode(userVariables));
    }

    private static void learnOperators() {
        System.out.println("\n--- Operators ---");
        System.out.println("Java has several types of operators:");
        
        String[][] operators = {
            {"Arithmetic", "+, -, *, /, %, ++, --"},
            {"Relational", "==, !=, >, <, >=, <="},
            {"Logical", "&&, ||, !"},
            {"Assignment", "=, +=, -=, *=, /=, %="},
            {"Bitwise", "&, |, ^, ~, <<, >>, >>>"}
        };
        
        for (String[] operator : operators) {
            System.out.println(operator[0] + ": " + operator[1]);
        }
        
        System.out.println("\nLet's practice with arithmetic operators!");
        int a = getIntInput("Enter a number for 'a': ");
        int b = getIntInput("Enter a number for 'b': ");
        
        System.out.println("a + b = " + (a + b));
        System.out.println("a - b = " + (a - b));
        System.out.println("a * b = " + (a * b));
        System.out.println("a / b = " + (a / b) + " (integer division)");
        System.out.println("a % b = " + (a % b) + " (remainder)");
        
        System.out.println("\nNow, let's try a compound expression:");
        String expression = getUserInput("Enter an expression using a and b (e.g., a * (b + 5)): ");
        try {
            double result = evaluateExpression(expression.replace("a", String.valueOf(a)).replace("b", String.valueOf(b)));
            System.out.println("Result: " + result);
        } catch (Exception e) {
            System.out.println("Sorry, I couldn't evaluate that expression.");
        }
    }

    private static void learnControlFlow() {
        System.out.println("\n--- Control Flow ---");
        System.out.println("Control flow statements direct the order of execution in a program.");
        
        System.out.println("\n1. If-Else Statement:");
        String ifElseExample = 
            "if (condition) {\n" +
            "    // code if condition is true\n" +
            "} else {\n" +
            "    // code if condition is false\n" +
            "}";
        System.out.println(ifElseExample);
        
        System.out.println("\n2. For Loop:");
        String forLoopExample = 
            "for (int i = 0; i < 5; i++) {\n" +
            "    System.out.println(i);\n" +
            "}";
        System.out.println(forLoopExample);
        
        System.out.println("\n3. While Loop:");
        String whileLoopExample = 
            "int i = 0;\n" +
            "while (i < 5) {\n" +
            "    System.out.println(i);\n" +
            "    i++;\n" +
            "}";
        System.out.println(whileLoopExample);
        
        System.out.println("\n4. Switch Statement:");
        String switchExample = 
            "switch (variable) {\n" +
            "    case value1:\n" +
            "        // code\n" +
            "        break;\n" +
            "    case value2:\n" +
            "        // code\n" +
            "        break;\n" +
            "    default:\n" +
            "        // code\n" +
            "}";
        System.out.println(switchExample);
        
        System.out.println("\nLet's practice! Write a program that prints numbers from 1 to 5 using a for loop:");
        String userLoop = getUserMultiLineInput();
        System.out.println("\nGreat! Here's how your loop looks:");
        System.out.println(formatJavaCode(userLoop));
    }

    private static void learnArraysAndCollections() {
        System.out.println("\n--- Arrays and Collections ---");
        
        System.out.println("Arrays are fixed-size sequences of elements of the same type.");
        String arrayExample = 
            "int[] numbers = new int[5];\n" +
            "numbers[0] = 1;\n" +
            "numbers[1] = 2;\n" +
            "// ...\n\n" +
            "// Or initialize directly:\n" +
            "int[] numbers = {1, 2, 3, 4, 5};";
        System.out.println(arrayExample);
        
        System.out.println("\nCollections are more flexible and provide various implementations:");
        System.out.println("1. ArrayList: Dynamic array");
        System.out.println("2. LinkedList: Doubly-linked list");
        System.out.println("3. HashSet: Unique elements, no order");
        System.out.println("4. HashMap: Key-value pairs");
        
        String collectionExample = 
            "import java.util.*;\n\n" +
            "List<String> names = new ArrayList<>();\n" +
            "names.add(\"Alice\");\n" +
            "names.add(\"Bob\");\n" +
            "System.out.println(names.get(0));  // Prints: Alice\n\n" +
            "Map<String, Integer> ages = new HashMap<>();\n" +
            "ages.put(\"Alice\", 30);\n" +
            "ages.put(\"Bob\", 25);\n" +
            "System.out.println(ages.get(\"Alice\"));  // Prints: 30";
        System.out.println("\nExample:");
        System.out.println(collectionExample);
        
        System.out.println("\nLet's practice! Create an array of your favorite colors:");
        String userArray = getUserMultiLineInput();
        System.out.println("\nGreat! Here's how your array looks:");
        System.out.println(formatJavaCode(userArray));
    }

    private static void learnOOPBasics() {
        System.out.println("\n--- Object-Oriented Programming Basics ---");
        System.out.println("OOP is based on the concept of 'objects' that contain data and code.");
        
        System.out.println("\nKey OOP concepts:");
        System.out.println("1. Encapsulation: Bundling data and methods that operate on that data");
        System.out.println("2. Inheritance: A class can inherit properties and methods from another class");
        System.out.println("3. Polymorphism: The ability of different classes to be treated as instances of the same class");
        
        String classExample = 
            "public class Car {\n" +
            "    private String model;\n" +
            "    private int year;\n\n" +
            "    public Car(String model, int year) {\n" +
            "        this.model = model;\n" +
            "        this.year = year;\n" +
            "    }\n\n" +
            "    public void start() {\n" +
            "        System.out.println(\"The \" + year + \" \" + model + \" is starting.\");\n" +
            "    }\n" +
            "}";
        System.out.println("\nHere's an example of a simple class:");
        System.out.println(classExample);
        
        System.out.println("\nLet's practice! Create a simple class representing a Book with title and author properties:");
        String userClass = getUserMultiLineInput();
        System.out.println("\nGreat! Here's how your class looks:");
        System.out.println(formatJavaCode(userClass));
    }

    private static void learnExceptionHandling() {
        System.out.println("\n--- Exception Handling ---");
        System.out.println("Exception handling allows you to manage runtime errors gracefully.");
        
        String exceptionExample = 
            "try {\n" +
            "    // Code that may throw an exception\n" +
            "    int result = 10 / 0;\n" +
            "} catch (ArithmeticException e) {\n" +
            "    System.out.println(\"Cannot divide by zero!\");\n" +
            "} finally {\n" +
            "    System.out.println(\"This always executes.\");\n" +
            "}";
        System.out.println("\nHere's an example of exception handling:");
        System.out.println(exceptionExample);
        
        System.out.println("\nCommon exceptions:");
        System.out.println("1. NullPointerException: Trying to use a null object reference");
        System.out.println("2. ArrayIndexOutOfBoundsException: Accessing an array element with an illegal index");
        System.out.println("3. FileNotFoundException: Attempt to access a file that does not exist");
        
        System.out.println("\nLet's practice! Write a try-catch block to handle dividing by zero:");
        String userException = getUserMultiLineInput();
        System.out.println("\nGreat! Here's how your exception handling looks:");
        System.out.println(formatJavaCode(userException));
    }

    private static void learnFileIO() {
        System.out.println("\n--- File I/O ---");
        System.out.println("Java provides various ways to read from and write to files.");
        
        String fileIOExample = 
            "import java.io.*;\n\n" +
            "// Writing to a file\n" +
            "try (FileWriter writer = new FileWriter(\"output.txt\")) {\n" +
            "    writer.write(\"Hello, World!\");\n" +
            "} catch (IOException e) {\n" +
            "    e.printStackTrace();\n" +
            "}\n\n" +
            "// Reading from a file\n" +
            "try (BufferedReader reader = new BufferedReader(new FileReader(\"input.txt\"))) {\n" +
            "    String line;\n" +
            "    while ((line = reader.readLine()) != null) {\n" +
            "        System.out.println(line);\n" +
            "    }\n" +
            "} catch (IOException e) {\n" +
            "    e.printStackTrace();\n" +
            "}";
        System.out.println("\nHere's an example of file I/O:");
        System.out.println(fileIOExample);
        
        System.out.println("\nKey points:");
        System.out.println("1. Always close your resources (or use try-with-resources)");
        System.out.println("2. Handle potential IOExceptions");
        System.out.println("3. Use buffered readers/writers for efficiency with larger files");
        
        System.out.println("\nLet's practice! Write code to create a file and write a message to it:");
        String userFileIO = getUserMultiLineInput();
        System.out.println("\nGreat! Here's how your file I/O code looks:");
        System.out.println(formatJavaCode(userFileIO));
    }

    private static String getUserInput(String prompt) {
        System.out.print(prompt + " ");
        return scanner.nextLine().trim();
    }

    private static String getUserMultiLineInput() {
        System.out.println("Enter your code (type 'END' on a new line when finished):");
        StringBuilder sb = new StringBuilder();
        String line;
        while (!(line = scanner.nextLine()).equals("END")) {
            sb.append(line).append("\n");
        }
        return sb.toString().trim();
    }

    private static int getIntInput(String prompt) {
        while (true) {
            try {
                return Integer.parseInt(getUserInput(prompt));
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid integer.");
            }
        }
    }

    private static double evaluateExpression(String expression) throws ScriptException {
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("JavaScript");
        
        if (engine == null) {
            throw new RuntimeException("JavaScript engine not found");
        }
        
        Object result = engine.eval(expression);
        
        if (result instanceof Number) {
            return ((Number) result).doubleValue();
        } else {
            throw new RuntimeException("Expression did not evaluate to a number");
        }
    }

    private static String formatJavaCode(String code) {
        String[] lines = code.split("\n");
        StringBuilder formattedCode = new StringBuilder();
        int indentLevel = 0;
        
        for (String line : lines) {
            line = line.trim();
            if (line.endsWith("}")) indentLevel = Math.max(0, indentLevel - 1);
            formattedCode.append("    ".repeat(indentLevel)).append(line).append("\n");
            if (line.endsWith("{")) indentLevel++;
        }
        
        return formattedCode.toString();
    }
}