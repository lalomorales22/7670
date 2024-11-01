import java.util.Scanner;
import javax.script.ScriptEngineManager;
import javax.script.ScriptEngine;
import javax.script.ScriptException;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.List;

public class EnhancedJavaLearningProgram {
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("Welcome to the Enhanced Interactive Java Learning Program!");
        
        while (true) {
            System.out.println("\nChoose a topic to learn about:");
            System.out.println("1. Variables and Data Types");
            System.out.println("2. Operators and Expressions");
            System.out.println("3. Control Flow Statements");
            System.out.println("4. Arrays and Collections");
            System.out.println("5. Methods and Functions");
            System.out.println("6. Object-Oriented Programming Basics");
            System.out.println("7. Exception Handling");
            System.out.println("8. File I/O Basics");
            System.out.println("9. Exit");
            
            int choice = getIntInput("Enter your choice (1-9): ");
            
            switch (choice) {
                case 1:
                    learnVariablesAndDataTypes();
                    break;
                case 2:
                    learnOperatorsAndExpressions();
                    break;
                case 3:
                    learnControlFlowStatements();
                    break;
                case 4:
                    learnArraysAndCollections();
                    break;
                case 5:
                    learnMethodsAndFunctions();
                    break;
                case 6:
                    learnOOPBasics();
                    break;
                case 7:
                    learnExceptionHandling();
                    break;
                case 8:
                    learnFileIOBasics();
                    break;
                case 9:
                    System.out.println("Thank you for using the Enhanced Java Learning Program. Goodbye!");
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    private static void learnVariablesAndDataTypes() {
        System.out.println("\n--- Variables and Data Types ---");
        System.out.println("Variables are containers for storing data values.");
        System.out.println("Java has two categories of data types:");
        System.out.println("1. Primitive data types");
        System.out.println("2. Reference data types");
        
        System.out.println("\nPrimitive Data Types:");
        String[][] primitiveTypes = {
            {"byte", "8-bit signed two's complement integer"},
            {"short", "16-bit signed two's complement integer"},
            {"int", "32-bit signed two's complement integer"},
            {"long", "64-bit signed two's complement integer"},
            {"float", "32-bit IEEE 754 floating-point"},
            {"double", "64-bit IEEE 754 floating-point"},
            {"boolean", "true or false"},
            {"char", "16-bit Unicode character"}
        };
        
        for (String[] type : primitiveTypes) {
            System.out.println("- " + type[0] + ": " + type[1]);
        }
        
        System.out.println("\nReference Data Types:");
        System.out.println("- Objects (e.g., String, Arrays, user-defined classes)");
        
        System.out.println("\nLet's practice declaring variables:");
        System.out.println("int age = 25;");
        System.out.println("double salary = 50000.50;");
        System.out.println("boolean isStudent = true;");
        System.out.println("String name = \"John Doe\";");
        
        System.out.println("\nNow you try! Declare a variable of any type:");
        String userDeclaration = scanner.nextLine().trim();
        System.out.println("Great! You've declared: " + userDeclaration);
    }

    private static void learnOperatorsAndExpressions() {
        System.out.println("\n--- Operators and Expressions ---");
        System.out.println("Operators are special symbols that perform specific operations on one, two, or three operands, and then return a result.");
        
        System.out.println("\nTypes of Operators:");
        System.out.println("1. Arithmetic Operators: +, -, *, /, %, ++, --");
        System.out.println("2. Relational Operators: ==, !=, >, <, >=, <=");
        System.out.println("3. Logical Operators: &&, ||, !");
        System.out.println("4. Assignment Operators: =, +=, -=, *=, /=, %=");
        System.out.println("5. Bitwise Operators: &, |, ^, ~, <<, >>, >>>");
        
        System.out.println("\nLet's practice with arithmetic operators:");
        int a = 10, b = 5;
        System.out.println("Given: int a = 10, b = 5");
        System.out.println("a + b = " + (a + b));
        System.out.println("a - b = " + (a - b));
        System.out.println("a * b = " + (a * b));
        System.out.println("a / b = " + (a / b));
        System.out.println("a % b = " + (a % b));
        
        System.out.println("\nNow, let's try a complex expression:");
        System.out.println("Expression: 2 + 3 * 4 - 6 / 2");
        int result = 2 + 3 * 4 - 6 / 2;
        System.out.println("Result: " + result);
        System.out.println("Explanation: First, 3 * 4 is evaluated (12), then 6 / 2 (3), finally 2 + 12 - 3 = 11");
        
        System.out.println("\nYour turn! Enter a simple arithmetic expression:");
        String userExpression = scanner.nextLine().trim();
        try {
            double userResult = evaluateExpression(userExpression);
            System.out.println("The result of your expression is: " + userResult);
        } catch (Exception e) {
            System.out.println("Sorry, I couldn't evaluate that expression. Make sure it's valid Java syntax!");
        }
    }

    private static void learnControlFlowStatements() {
        System.out.println("\n--- Control Flow Statements ---");
        System.out.println("Control flow statements allow you to control the flow of your program's execution based on certain conditions.");
        
        System.out.println("\n1. If-Else Statement:");
        System.out.println("if (condition) {");
        System.out.println("    // code to be executed if condition is true");
        System.out.println("} else {");
        System.out.println("    // code to be executed if condition is false");
        System.out.println("}");
        
        System.out.println("\n2. Switch Statement:");
        System.out.println("switch (expression) {");
        System.out.println("    case value1:");
        System.out.println("        // code");
        System.out.println("        break;");
        System.out.println("    case value2:");
        System.out.println("        // code");
        System.out.println("        break;");
        System.out.println("    default:");
        System.out.println("        // code");
        System.out.println("}");
        
        System.out.println("\n3. For Loop:");
        System.out.println("for (initialization; condition; update) {");
        System.out.println("    // code to be repeated");
        System.out.println("}");
        
        System.out.println("\n4. While Loop:");
        System.out.println("while (condition) {");
        System.out.println("    // code to be repeated");
        System.out.println("}");
        
        System.out.println("\n5. Do-While Loop:");
        System.out.println("do {");
        System.out.println("    // code to be repeated");
        System.out.println("} while (condition);");
        
        System.out.println("\nLet's practice with a for loop. We'll print numbers from 1 to 5:");
        for (int i = 1; i <= 5; i++) {
            System.out.print(i + " ");
        }
        
        System.out.println("\n\nNow you try! Enter a number, and we'll count down from that number to 1:");
        int userNumber = getIntInput("Enter a positive integer: ");
        for (int i = userNumber; i >= 1; i--) {
            System.out.print(i + " ");
        }
        System.out.println();
    }

    private static void learnArraysAndCollections() {
        System.out.println("\n--- Arrays and Collections ---");
        System.out.println("Arrays and Collections are used to store multiple values in a single variable.");
        
        System.out.println("\nArrays:");
        System.out.println("An array is a fixed-size container that holds values of the same type.");
        System.out.println("Declaration: int[] numbers = new int[5];");
        System.out.println("Initialization: int[] numbers = {1, 2, 3, 4, 5};");
        
        int[] exampleArray = {10, 20, 30, 40, 50};
        System.out.println("\nExample Array: " + Arrays.toString(exampleArray));
        System.out.println("Access element: exampleArray[2] = " + exampleArray[2]);
        System.out.println("Array length: exampleArray.length = " + exampleArray.length);
        
        System.out.println("\nCollections:");
        System.out.println("Collections are dynamic data structures in Java.");
        System.out.println("Common interfaces: List, Set, Map");
        
        System.out.println("\nArrayList (implements List):");
        List<String> fruits = new ArrayList<>();
        fruits.add("Apple");
        fruits.add("Banana");
        fruits.add("Cherry");
        System.out.println("ArrayList: " + fruits);
        System.out.println("Add element: fruits.add(\"Date\")");
        fruits.add("Date");
        System.out.println("Updated ArrayList: " + fruits);
        System.out.println("Remove element: fruits.remove(\"Banana\")");
        fruits.remove("Banana");
        System.out.println("Final ArrayList: " + fruits);
        
        System.out.println("\nNow you try! Let's create an array of your favorite colors.");
        System.out.print("How many colors do you want to add? ");
        int numColors = getIntInput("Enter a number: ");
        String[] userColors = new String[numColors];
        
        for (int i = 0; i < numColors; i++) {
            System.out.print("Enter color #" + (i+1) + ": ");
            userColors[i] = scanner.nextLine().trim();
        }
        
        System.out.println("Your color array: " + Arrays.toString(userColors));
    }

    private static void learnMethodsAndFunctions() {
        System.out.println("\n--- Methods and Functions ---");
        System.out.println("Methods are blocks of code that perform a specific task. They are used to organize code, make it reusable, and make it easier to read and maintain.");
        
        System.out.println("\nMethod Structure:");
        System.out.println("accessModifier returnType methodName(parameterList) {");
        System.out.println("    // method body");
        System.out.println("    return returnValue; // if applicable");
        System.out.println("}");
        
        System.out.println("\nExample Method:");
        System.out.println("public static int add(int a, int b) {");
        System.out.println("    return a + b;");
        System.out.println("}");
        
        System.out.println("\nLet's use our add method:");
        int sum = add(5, 3);
        System.out.println("add(5, 3) returns: " + sum);
        
        System.out.println("\nMethod Overloading:");
        System.out.println("Java allows methods with the same name but different parameter lists.");
        System.out.println("Example:");
        System.out.println("public static double add(double a, double b) {");
        System.out.println("    return a + b;");
        System.out.println("}");
        
        double doubleSum = add(2.5, 3.7);
        System.out.println("add(2.5, 3.7) returns: " + doubleSum);
        
        System.out.println("\nNow you try! Let's create a simple calculator method.");
        System.out.println("Enter two numbers and an operation (+, -, *, /):");
        double num1 = getDoubleInput("Enter first number: ");
        double num2 = getDoubleInput("Enter second number: ");
        System.out.print("Enter operation (+, -, *, /): ");
        String operation = scanner.nextLine().trim();
        
        try {
            double result = calculate(num1, num2, operation);
            System.out.println("Result: " + result);
        } catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
        }
    }

    private static int add(int a, int b) {
        return a + b;
    }

    private static double add(double a, double b) {
        return a + b;
    }

    private static double calculate(double a, double b, String operation) {
        switch (operation) {
            case "+":
                return a + b;
            case "-":
                return a - b;
            case "*":
                return a * b;
            case "/":
                if (b == 0) throw new IllegalArgumentException("Cannot divide by zero");
                return a / b;
            default:
                throw new IllegalArgumentException("Invalid operation");
        }
    }

    private static void learnOOPBasics() {
        System.out.println("\n--- Object-Oriented Programming Basics ---");
        System.out.println("Object-Oriented Programming (OOP) is a programming paradigm based on the concept of 'objects'.");
        System.out.println("The four main principles of OOP are:");
        System.out.println("1. Encapsulation");
        System.out.println("2. Inheritance");
        System.out.println("3. Polymorphism");
        System.out.println("4. Abstraction");
        
        System.out.println("\nLet's create a simple class hierarchy to demonstrate these concepts:");
        
        System.out.println("// Base class");
        System.out.println("public class Animal {");
        System.out.println("    private String name;  // Encapsulation");
        System.out.println("    ");
        System.out.println("    public Animal(String name) {");
        System.out.println("        this.name = name;");
        System.out.println("    }");
        System.out.println("    ");
        System.out.println("    public void makeSound() {  // Polymorphism");
        System.out.println("        System.out.println(\"The animal makes a sound\");");
        System.out.println("    }");
        System.out.println("    ");
        System.out.println("    public String getName() {  // Getter method");
        System.out.println("        return name;");
        System.out.println("    }");
        System.out.println("}");
        
        System.out.println("\n// Derived class (Inheritance)");
        System.out.println("public class Dog extends Animal {");
        System.out.println("    public Dog(String name) {");
        System.out.println("        super(name);");
        System.out.println("    }");
        System.out.println("    ");
        System.out.println("    @Override");
        System.out.println("    public void makeSound() {  // Method overriding (Polymorphism)");
        System.out.println("        System.out.println(\"The dog barks\");");
        System.out.println("    }");
        System.out.println("}");
        
        System.out.println("\nNow, let's create instances of these classes and demonstrate OOP concepts:");
        
        Animal genericAnimal = new Animal("Generic Animal");
        Dog dog = new Dog("Buddy");
        
        System.out.println("genericAnimal.getName(): " + genericAnimal.getName());
        System.out.print("genericAnimal.makeSound(): ");
        genericAnimal.makeSound();
        
        System.out.println("dog.getName(): " + dog.getName());
        System.out.print("dog.makeSound(): ");
        dog.makeSound();
        
        System.out.println("\nPolymorphism example:");
        Animal polymorphicAnimal = new Dog("Rex");
        System.out.print("polymorphicAnimal.makeSound(): ");
        polymorphicAnimal.makeSound();
        
        System.out.println("\nNow you try! Let's create a simple class.");
        System.out.print("Enter a class name: ");
        String className = scanner.nextLine().trim();
        System.out.print("Enter an attribute name: ");
        String attributeName = scanner.nextLine().trim();
        System.out.print("Enter a method name: ");
        String methodName = scanner.nextLine().trim();
        
        System.out.println("\nHere's your class:");
        System.out.println("public class " + className + " {");
        System.out.println("    private String " + attributeName + ";");
        System.out.println("    ");
        System.out.println("    public " + className + "(String " + attributeName + ") {");
        System.out.println("        this." + attributeName + " = " + attributeName + ";");
        System.out.println("    }");
        System.out.println("    ");
        System.out.println("    public void " + methodName + "() {");
        System.out.println("        System.out.println(\"This is the " + methodName + " method\");");
        System.out.println("    }");
        System.out.println("}");
    }

    private static void learnExceptionHandling() {
        System.out.println("\n--- Exception Handling ---");
        System.out.println("Exception handling is a mechanism to handle runtime errors and maintain the normal flow of the application.");
        
        System.out.println("\nTry-Catch Block:");
        System.out.println("try {");
        System.out.println("    // Code that may throw an exception");
        System.out.println("} catch (ExceptionType e) {");
        System.out.println("    // Code to handle the exception");
        System.out.println("}");
        
        System.out.println("\nMultiple Catch Blocks:");
        System.out.println("try {");
        System.out.println("    // Code that may throw exceptions");
        System.out.println("} catch (ExceptionType1 e) {");
        System.out.println("    // Handle ExceptionType1");
        System.out.println("} catch (ExceptionType2 e) {");
        System.out.println("    // Handle ExceptionType2");
        System.out.println("}");
        
        System.out.println("\nFinally Block:");
        System.out.println("try {");
        System.out.println("    // Code that may throw an exception");
        System.out.println("} catch (ExceptionType e) {");
        System.out.println("    // Handle the exception");
        System.out.println("} finally {");
        System.out.println("    // Code that always executes");
        System.out.println("}");
        
        System.out.println("\nLet's practice exception handling. We'll try to convert a string to an integer:");
        System.out.print("Enter a number (or any text): ");
        String userInput = scanner.nextLine().trim();
        
        try {
            int number = Integer.parseInt(userInput);
            System.out.println("Successfully converted to int: " + number);
        } catch (NumberFormatException e) {
            System.out.println("Exception caught: " + e.getMessage());
            System.out.println("The input couldn't be converted to an integer.");
        } finally {
            System.out.println("This finally block always executes.");
        }
    }

    private static void learnFileIOBasics() {
        System.out.println("\n--- File I/O Basics ---");
        System.out.println("File I/O (Input/Output) allows you to read from and write to files on your computer.");
        
        System.out.println("\nWriting to a File:");
        System.out.println("try (FileWriter writer = new FileWriter(\"example.txt\")) {");
        System.out.println("    writer.write(\"Hello, File I/O!\");");
        System.out.println("} catch (IOException e) {");
        System.out.println("    e.printStackTrace();");
        System.out.println("}");
        
        System.out.println("\nReading from a File:");
        System.out.println("try (Scanner fileScanner = new Scanner(new File(\"example.txt\"))) {");
        System.out.println("    while (fileScanner.hasNextLine()) {");
        System.out.println("        String line = fileScanner.nextLine();");
        System.out.println("        System.out.println(line);");
        System.out.println("    }");
        System.out.println("} catch (IOException e) {");
        System.out.println("    e.printStackTrace();");
        System.out.println("}");
        
        System.out.println("\nLet's practice file I/O. We'll write a message to a file and then read it back.");
        System.out.print("Enter a message to write to a file: ");
        String message = scanner.nextLine();
        
        String fileName = "user_message.txt";
        
        // Writing to file
        try (FileWriter writer = new FileWriter(fileName)) {
            writer.write(message);
            System.out.println("Message written to " + fileName);
        } catch (IOException e) {
            System.out.println("An error occurred while writing to the file.");
            e.printStackTrace();
        }
        
        // Reading from file
        System.out.println("\nNow, let's read the message back from the file:");
        try (Scanner fileScanner = new Scanner(new File(fileName))) {
            while (fileScanner.hasNextLine()) {
                String line = fileScanner.nextLine();
                System.out.println("Read from file: " + line);
            }
        } catch (IOException e) {
            System.out.println("An error occurred while reading the file.");
            e.printStackTrace();
        }
    }

    private static int getIntInput(String prompt) {
        while (true) {
            System.out.print(prompt);
            try {
                return Integer.parseInt(scanner.nextLine().trim());
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid integer.");
            }
        }
    }

    private static double getDoubleInput(String prompt) {
        while (true) {
            System.out.print(prompt);
            try {
                return Double.parseDouble(scanner.nextLine().trim());
            } catch (NumberFormatException e) {
                System.out.println("Please enter a valid number.");
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
}

class Animal {
    private String name;

    public Animal(String name) {
        this.name = name;
    }

    public void makeSound() {
        System.out.println("The animal makes a sound");
    }

    public String getName() {
        return name;
    }
}

class Dog extends Animal {
    public Dog(String name) {
        super(name);
    }

    @Override
    public void makeSound() {
        System.out.println("The dog barks");
    }
}