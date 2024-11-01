import java.util.*;

/**
 * JavaTutorial: An interactive game to learn Java programming concepts
 * This class represents the main game logic and flow.
 */
public class JavaTutorial {
    private static Scanner scanner = new Scanner(System.in);
    private static Random random = new Random();
    private static int playerHealth = 100;
    private static int playerExperience = 0;
    private static List<String> inventory = new ArrayList<>();

    /**
     * Main method: Entry point of the program
     * @param args Command line arguments (not used in this program)
     */
    public static void main(String[] args) {
        System.out.println("Welcome to the Epic Java Adventure: Quest for the Golden Compiler!");
        System.out.println("This interactive game will teach you Java programming concepts as you progress.");
        System.out.print("Enter your name, brave programmer: ");
        String playerName = scanner.nextLine();

        System.out.println("\nGreetings, " + playerName + "! You find yourself in the mystical land of Javania.");
        System.out.println("Your quest is to find the legendary Golden Compiler, which is said to grant unlimited coding power.");
        System.out.println("But beware! The path is treacherous and filled with coding challenges. Are you ready to begin?");

        boolean continuePlaying = true;
        while (continuePlaying && playerHealth > 0) {
            int choice = displayMainMenu();
            switch (choice) {
                case 1:
                    exploreBasicLands();
                    break;
                case 2:
                    ventureIntoOOPForest();
                    break;
                case 3:
                    traverseDataStructureMountains();
                    break;
                case 4:
                    navigateExceptionSwamp();
                    break;
                case 5:
                    enterAdvancedRealm();
                    break;
                case 6:
                    viewPlayerStatus();
                    break;
                case 7:
                    learnJavaConcepts();
                    break;
                case 8:
                    practiceJavaExercises();
                    break;
                case 9:
                    continuePlaying = false;
                    break;
            }
        }

        if (playerHealth <= 0) {
            System.out.println("\nOh no! Your health has reached zero. Game over!");
        }

        System.out.println("\nThank you for playing, " + playerName + "!");
        System.out.println("Final Experience Points: " + playerExperience);
        System.out.println("Items collected: " + inventory);
        System.out.println("We hope you learned a lot about Java programming. Keep coding and exploring!");
    }

    /**
     * Displays the main menu and returns the user's choice
     * @return An integer representing the user's menu choice
     */
    private static int displayMainMenu() {
        System.out.println("\n--- Main Menu ---");
        System.out.println("1. Explore the Basic Lands (Variables, Data Types, Control Flow)");
        System.out.println("2. Venture into the OOP Forest (Classes, Objects, Inheritance)");
        System.out.println("3. Traverse the Data Structure Mountains (Arrays, Lists, Maps)");
        System.out.println("4. Navigate the Exception Swamp (Error Handling)");
        System.out.println("5. Enter the Advanced Realm (Threads, Lambdas, Generics)");
        System.out.println("6. View Player Status");
        System.out.println("7. Learn Java Concepts (Tutorial Mode)");
        System.out.println("8. Practice Java Exercises");
        System.out.println("9. Exit Game");
        System.out.print("Enter your choice (1-9): ");
        return scanner.nextInt();
    }

    /**
     * Explores the basic concepts of Java programming
     */
    private static void exploreBasicLands() {
        System.out.println("\n=== The Basic Lands of Javania ===");
        System.out.println("You enter a serene valley where the fundamentals of Java reside.");
        
        // Variables and Data Types Challenge
        System.out.println("\nA wise sage approaches you and asks about Java's primitive data types.");
        System.out.println("In Java, primitive data types are the most basic data types available.");
        System.out.println("They are the building blocks of data manipulation and are used to declare variables.");
        String[] dataTypes = {"byte", "short", "int", "long", "float", "double", "boolean", "char"};
        List<String> remainingTypes = new ArrayList<>(Arrays.asList(dataTypes));
        int correctAnswers = 0;

        System.out.println("Can you name all 8 primitive data types in Java? (Enter one at a time)");
        for (int i = 0; i < 8; i++) {
            System.out.print("Enter a data type: ");
            String answer = scanner.next().toLowerCase();
            if (remainingTypes.remove(answer)) {
                System.out.println("Correct! " + explainDataType(answer));
                correctAnswers++;
            } else {
                System.out.println("Incorrect or already mentioned.");
            }
        }
        System.out.println("You correctly named " + correctAnswers + " out of 8 primitive data types.");
        playerExperience += correctAnswers * 5;

        // Control Flow Challenge
        System.out.println("\nYou encounter a mystical gate with three levers.");
        System.out.println("To pass, you must demonstrate your knowledge of control flow statements.");
        System.out.println("Control flow statements regulate the order in which a program's code executes.");
        System.out.println("Which of these is NOT a looping structure in Java?");
        System.out.println("1. for");
        System.out.println("2. while");
        System.out.println("3. do-while");
        System.out.println("4. repeat-until");
        int answer = scanner.nextInt();
        if (answer == 4) {
            System.out.println("Correct! The gate opens, allowing you to pass.");
            System.out.println("Java uses for, while, and do-while loops. There is no repeat-until loop in Java.");
            System.out.println("Here's a quick example of each valid loop:");
            System.out.println("for (int i = 0; i < 5; i++) { /* code */ }");
            System.out.println("while (condition) { /* code */ }");
            System.out.println("do { /* code */ } while (condition);");
            playerExperience += 15;
        } else {
            System.out.println("Incorrect. The correct answer was 'repeat-until'. You take 10 damage as the gate zaps you.");
            System.out.println("Remember, Java uses for, while, and do-while loops.");
            playerHealth -= 10;
        }

        // Arrays and String Manipulation
        System.out.println("\nYou find a magical scroll with scrambled letters.");
        System.out.println("This challenge will test your understanding of arrays and string manipulation.");
        String[] words = {"java", "programming", "array", "string", "method"};
        String chosenWord = words[random.nextInt(words.length)];
        char[] scrambledWord = chosenWord.toCharArray();
        for (int i = 0; i < scrambledWord.length; i++) {
            int j = random.nextInt(scrambledWord.length);
            char temp = scrambledWord[i];
            scrambledWord[i] = scrambledWord[j];
            scrambledWord[j] = temp;
        }
        System.out.println("Unscramble this word: " + new String(scrambledWord));
        String playerGuess = scanner.next().toLowerCase();
        if (playerGuess.equals(chosenWord)) {
            System.out.println("Correct! You've mastered array and string manipulation.");
            System.out.println("Here's what happened behind the scenes:");
            System.out.println("1. We converted the string to a char array using toCharArray()");
            System.out.println("2. We shuffled the array using a simple swap algorithm");
            System.out.println("3. We converted the char array back to a string using new String(char[])");
            playerExperience += 20;
            inventory.add("Magic Scroll");
        } else {
            System.out.println("Incorrect. The word was: " + chosenWord);
            System.out.println("Don't worry! String manipulation takes practice. Keep trying!");
        }
    }

    /**
     * Explains a given primitive data type
     * @param dataType The name of the data type to explain
     * @return A string explanation of the data type
     */
    private static String explainDataType(String dataType) {
        switch (dataType) {
            case "byte":
                return "byte: 8-bit signed two's complement integer. Range: -128 to 127";
            case "short":
                return "short: 16-bit signed two's complement integer. Range: -32,768 to 32,767";
            case "int":
                return "int: 32-bit signed two's complement integer. Range: -2^31 to 2^31-1";
            case "long":
                return "long: 64-bit signed two's complement integer. Range: -2^63 to 2^63-1";
            case "float":
                return "float: single-precision 32-bit IEEE 754 floating point";
            case "double":
                return "double: double-precision 64-bit IEEE 754 floating point";
            case "boolean":
                return "boolean: true or false";
            case "char":
                return "char: single 16-bit Unicode character. Range: '\\u0000' to '\\uffff'";
            default:
                return "Unknown data type";
        }
    }

    /**
     * Explores Object-Oriented Programming concepts
     */
    private static void ventureIntoOOPForest() {
        System.out.println("\n=== The Object-Oriented Programming Forest ===");
        System.out.println("You enter a lush forest where objects come to life and inheritance is the law of the land.");
        System.out.println("Object-Oriented Programming (OOP) is a programming paradigm based on the concept of 'objects'.");
        System.out.println("Objects can contain data and code: data in the form of fields, and code in the form of procedures.");

        // Class and Object Creation
        System.out.println("\nA mystical creature appears and challenges you to create a 'Spell' class.");
        System.out.println("In Java, a class is a blueprint for creating objects.");
        System.out.println("Which of the following correctly defines a class with a constructor?");
        System.out.println("1. class Spell { public Spell() {} }");
        System.out.println("2. Spell { constructor() {} }");
        System.out.println("3. public class Spell { Spell() }");
        int answer = scanner.nextInt();
        if (answer == 1) {
            System.out.println("Correct! You've successfully created the Spell class.");
            System.out.println("Let's break it down:");
            System.out.println("- 'class' keyword declares a new class");
            System.out.println("- 'Spell' is the name of the class");
            System.out.println("- 'public Spell()' is the constructor");
            System.out.println("- '{}' contain the body of the constructor");
            playerExperience += 20;
        } else {
            System.out.println("Incorrect. The proper way to define a class with a constructor is: class Spell { public Spell() {} }");
            System.out.println("Remember, constructors have the same name as the class and no return type.");
            playerHealth -= 5;
        }

        // Inheritance Challenge
        System.out.println("\nYou encounter a family of magical creatures teaching about inheritance.");
        System.out.println("Inheritance is a mechanism where you can derive a class from another class.");
        System.out.println("Complete the following code to make 'FireSpell' inherit from 'Spell':");
        System.out.println("public class FireSpell ___ Spell { }");
        System.out.print("Enter the missing keyword: ");
        String keyword = scanner.next();
        if (keyword.equalsIgnoreCase("extends")) {
            System.out.println("Excellent! You understand inheritance in Java.");
            System.out.println("The 'extends' keyword is used to inherit from a class.");
            System.out.println("FireSpell is now a subclass of Spell and inherits all its non-private members.");
            playerExperience += 25;
            inventory.add("Inheritance Tome");
        } else {
            System.out.println("Not quite. The correct keyword is 'extends'.");
            System.out.println("In Java, we use 'extends' to create a subclass.");
            playerHealth -= 5;
        }

        // Polymorphism Puzzle
        System.out.println("\nYou reach a clearing with shape-shifting creatures.");
        System.out.println("They challenge you to demonstrate your understanding of polymorphism.");
        System.out.println("Polymorphism allows objects to be treated as instances of their parent class.");
        System.out.println("Which statement about polymorphism is true?");
        System.out.println("1. It allows a class to have multiple superclasses");
        System.out.println("2. It enables a subclass to override methods from its superclass");
        System.out.println("3. It's a way to create multiple instances of the same class");
        answer = scanner.nextInt();
        if (answer == 2) {
            System.out.println("Correct! You've grasped the concept of polymorphism.");
            System.out.println("Polymorphism allows a subclass to provide a specific implementation of a method");
            System.out.println("that is already defined in its superclass. This is called method overriding.");
            System.out.println("Example:");
            System.out.println("class Animal { void makeSound() { System.out.println(\"Some sound\"); } }");
            System.out.println("class Dog extends Animal { void makeSound() { System.out.println(\"Bark\"); } }");
            playerExperience += 30;
        } else {
            System.out.println("Incorrect. Polymorphism allows a subclass to override methods from its superclass.");
            System.out.println("This enables objects of different types to be treated uniformly.");
            playerHealth -= 10;
        }
    }

    /**
     * Explores data structures and algorithms
     */
    private static void traverseDataStructureMountains() {
        System.out.println("\n=== The Data Structure Mountains ===");
        System.out.println("You begin climbing the treacherous peaks of data structures and algorithms.");
        System.out.println("Data structures are ways of organizing and storing data for efficient access and modification.");
        System.out.println("Algorithms are step-by-step procedures for solving problems or performing tasks.");

        // ArrayList Challenge
        System.out.println("\nYou encounter a dynamic cliff face that keeps changing.");
        System.out.println("To scale it, you must demonstrate your knowledge of ArrayLists.");
        System.out.println("ArrayList is a resizable array implementation of the List interface.");
        System.out.println("Which method is used to add an element to an ArrayList?");
        System.out.println("1. push()");
        System.out.println("2. append()");
        System.out.println("3. add()");
        int answer = scanner.nextInt();
        if (answer == 3) {
            System.out.println("Correct! You skillfully navigate the changing cliff.");
            System.out.println("The add() method is used to append an element to the end of an ArrayList.");
            System.out.println("Example: myList.add(element);");
            playerExperience += 25;
        } else {
            System.out.println("Incorrect. The method to add an element to an ArrayList is add().");
            System.out.println("Remember, ArrayLists are part of Java's Collections framework.");
            playerHealth -= 10;
        }

        // Sorting Algorithm Implementation
        System.out.println("\nYou reach a jumbled rock formation that needs sorting.");
        System.out.println("This challenge will test your understanding of sorting algorithms.");
        int[] rocks = {5, 2, 8, 12, 1, 6};
        System.out.println("Original formation: " + Arrays.toString(rocks));
        System.out.println("Implement a bubble sort to arrange these rocks. Enter the sorted array:");
        int[] playerSorted = new int[6];
        for (int i = 0; i < 6; i++) {
            playerSorted[i] = scanner.nextInt();
        }
        Arrays.sort(rocks);
        if (Arrays.equals(rocks, playerSorted)) {
            System.out.println("Perfect! You've mastered the bubble sort algorithm.");
            System.out.println("Bubble sort works by repeatedly stepping through the list, comparing adjacent elements and swapping them if they're in the wrong order.");
            System.out.println("Here's a simple implementation in Java:");
            System.out.println("for (int i = 0; i < arr.length - 1; i++) {");
            System.out.println("    for (int j = 0; j < arr.length - i - 1; j++) {");
            System.out.println("        if (arr[j] > arr[j+1]) {");
            System.out.println("            int temp = arr[j];");
            System.out.println("            arr[j] = arr[j+1];");
            System.out.println("            arr[j+1] = temp;");
            System.out.println("        }");
            System.out.println("    }");
            System.out.println("}");
            playerExperience += 40;
            inventory.add("Sorting Wand");
        } else {
            System.out.println("Not quite right. The correct sorting is: " + Arrays.toString(rocks));
            System.out.println("Don't worry! Sorting algorithms can be tricky. Keep practicing!");
            playerHealth -= 15;
        }

        // HashMap Usage
        System.out.println("\nYou find a magical map that requires understanding of HashMaps.");
        System.out.println("HashMap is a data structure that implements the Map interface and stores key-value pairs.");
        System.out.println("Complete the code to add a key-value pair to a HashMap:");
        System.out.println("HashMap<String, Integer> map = new HashMap<>();");
        System.out.println("map._____(\"treasure\", 100);");
        System.out.print("Enter the missing method name: ");
        String method = scanner.next();
        if (method.equalsIgnoreCase("put")) {
            System.out.println("Excellent! You've unlocked the secrets of the magical map.");
            System.out.println("The put() method is used to add a key-value pair to a HashMap.");
            System.out.println("If the key already exists, put() will update the value.");
            System.out.println("To retrieve a value: Integer value = map.get(\"treasure\");");
            playerExperience += 35;
        } else {
            System.out.println("Incorrect. The method to add a key-value pair to a HashMap is put().");
            System.out.println("Remember, HashMaps store key-value pairs for quick retrieval.");
            playerHealth -= 10;
        }
    }

    private static void navigateExceptionSwamp() {
        System.out.println("\n=== The Exception Swamp ===");
        System.out.println("You enter a murky swamp where exceptions lurk in every shadow.");
        System.out.println("Exceptions in Java are used to handle errors and other exceptional events.");

        // Try-Catch Challenge
        System.out.println("\nA rickety bridge appears before you. To cross safely, you must handle exceptions correctly.");
        System.out.println("Complete the following try-catch block:");
        System.out.println("try {");
        System.out.println("    // Risky code here");
        System.out.println("} _____ (Exception e) {");
        System.out.println("    // Handle exception");
        System.out.println("}");
        System.out.print("Enter the missing keyword: ");
        String keyword = scanner.next();
        if (keyword.equalsIgnoreCase("catch")) {
            System.out.println("Correct! You cross the bridge safely.");
            System.out.println("The try-catch block is used to handle exceptions in Java.");
            System.out.println("The code that might throw an exception goes in the try block.");
            System.out.println("The catch block specifies what to do if an exception occurs.");
            playerExperience += 30;
        } else {
            System.out.println("Incorrect. The proper keyword is 'catch'. You stumble and fall into the swamp.");
            System.out.println("Remember, try and catch always go together in exception handling.");
            playerHealth -= 20;
        }

        // Custom Exception
        System.out.println("\nYou encounter a magical barrier that requires creating a custom exception to pass.");
        System.out.println("Custom exceptions allow you to define application-specific error conditions.");
        System.out.println("How do you define a custom checked exception in Java?");
        System.out.println("1. class MyException implements Exception { }");
        System.out.println("2. class MyException extends RuntimeException { }");
        System.out.println("3. class MyException extends Exception { }");
        int answer = scanner.nextInt();
        if (answer == 3) {
            System.out.println("Excellent! You create the custom exception and pass through the barrier.");
            System.out.println("To create a custom checked exception, you extend the Exception class.");
            System.out.println("Checked exceptions must be declared in a method's throws clause or handled in a try-catch block.");
            System.out.println("Example usage:");
            System.out.println("public void myMethod() throws MyException {");
            System.out.println("    if (someCondition) {");
            System.out.println("        throw new MyException(\"Something went wrong\");");
            System.out.println("    }");
            System.out.println("}");
            playerExperience += 40;
            inventory.add("Exception Amulet");
        } else {
            System.out.println("Incorrect. To create a custom checked exception, you should extend the Exception class.");
            System.out.println("Remember, RuntimeException and its subclasses are unchecked exceptions.");
            playerHealth -= 15;
        }

        // Finally Block Usage
        System.out.println("\nYou reach a clearing where you must demonstrate your understanding of the 'finally' block.");
        System.out.println("The finally block is used to execute important code such as closing connections, streams etc.");
        System.out.println("When does the code in a 'finally' block execute?");
        System.out.println("1. Only if an exception is caught");
        System.out.println("2. Only if no exception occurs");
        System.out.println("3. Always, regardless of whether an exception occurs or is caught");
        answer = scanner.nextInt();
        if (answer == 3) {
            System.out.println("Correct! Your knowledge of 'finally' blocks helps you navigate the swamp safely.");
            System.out.println("The finally block always executes when the try block exits.");
            System.out.println("This ensures that important cleanup code is executed, even if an exception occurs.");
            System.out.println("Example:");
            System.out.println("try {");
            System.out.println("    // Some risky code");
            System.out.println("} catch (Exception e) {");
            System.out.println("    // Handle the exception");
            System.out.println("} finally {");
            System.out.println("    // This will always execute");
            System.out.println("}");
            playerExperience += 35;
        } else {
            System.out.println("Incorrect. The 'finally' block always executes, regardless of exceptions.");
            System.out.println("It's commonly used for cleanup operations that must be performed under any circumstances.");
            playerHealth -= 10;
        }
    }

    private static void enterAdvancedRealm() {
        System.out.println("\n=== The Advanced Realm ===");
        System.out.println("You step into a shimmering portal, entering the realm of advanced Java concepts.");

        // Multithreading Challenge
        System.out.println("\nYou encounter multiple paths that must be traversed simultaneously.");
        System.out.println("This challenge tests your knowledge of multithreading in Java.");
        System.out.println("Multithreading allows concurrent execution of two or more parts of a program.");
        System.out.println("Which interface should a class implement to create a thread in Java?");
        System.out.println("1. Threadable");
        System.out.println("2. Runnable");
        System.out.println("3. Threadable");
        int answer = scanner.nextInt();
        if (answer == 2) {
            System.out.println("Correct! You successfully navigate the multiple paths using threads.");
            System.out.println("The Runnable interface is used to create a thread in Java.");
            System.out.println("Example of creating and starting a thread:");
            System.out.println("class MyRunnable implements Runnable {");
            System.out.println("    public void run() {");
            System.out.println("        // Code to run in new thread");
            System.out.println("    }");
            System.out.println("}");
            System.out.println("Thread thread = new Thread(new MyRunnable());");
            System.out.println("thread.start();");
            playerExperience += 50;
        } else {
            System.out.println("Incorrect. The interface to implement for creating a thread is Runnable.");
            System.out.println("Remember, you can also extend the Thread class, but implementing Runnable is often preferred.");
            playerHealth -= 20;
        }

        // Lambda Expressions
        System.out.println("\nA mystical code appears, requiring knowledge of lambda expressions to decipher.");
        System.out.println("Lambda expressions provide a clear and concise way to implement functional interfaces.");
        System.out.println("Complete the lambda expression to create a simple addition function:");
        System.out.println("BiFunction<Integer, Integer, Integer> add = (a, b) -> _____;");
        System.out.print("Enter the missing part: ");
        String lambda = scanner.next();
        if (lambda.equals("a+b")) {
            System.out.println("Excellent! You've mastered lambda expressions.");
            System.out.println("Lambda expressions are a shorthand notation for anonymous functions.");
            System.out.println("They're particularly useful with functional interfaces.");
            System.out.println("Example usage:");
            System.out.println("int result = add.apply(5, 3); // Returns 8");
            playerExperience += 45;
            inventory.add("Lambda Codex");
        } else {
            System.out.println("Not quite. The correct lambda expression is: (a, b) -> a + b");
            System.out.println("This creates a function that takes two integers and returns their sum.");
            playerHealth -= 15;
        }

        // Generics
        System.out.println("\nYou reach a chamber filled with shape-shifting containers.");
        System.out.println("To proceed, demonstrate your understanding of generics.");
        System.out.println("Generics allow you to write code that works with different types while providing compile-time type safety.");
        System.out.println("What symbol is used to declare a generic type parameter?");
        System.out.print("Enter the symbol: ");
        String symbol = scanner.next();
        if (symbol.equals("<>") || symbol.equals("<")) {
            System.out.println("Correct! The containers adapt to your command, allowing passage.");
            System.out.println("Generics use angle brackets <> to specify type parameters.");
            System.out.println("Example of a generic class:");
            System.out.println("public class Box<T> {");
            System.out.println("    private T content;");
            System.out.println("    public void set(T content) { this.content = content; }");
            System.out.println("    public T get() { return content; }");
            System.out.println("}");
            System.out.println("Usage: Box<Integer> intBox = new Box<>();");
            playerExperience += 55;
        } else {
            System.out.println("Incorrect. The symbol for generic type parameters is <>.");
            System.out.println("Generics provide stronger type checks at compile time and eliminate the need for many type casts.");
            playerHealth -= 25;
        }
    }

    private static void viewPlayerStatus() {
        System.out.println("\n=== Player Status ===");
        System.out.println("Health: " + playerHealth);
        System.out.println("Experience: " + playerExperience);
        System.out.println("Inventory: " + inventory);
    }

    private static void learnJavaConcepts() {
        System.out.println("\n=== Java Concepts Tutorial ===");
        System.out.println("Welcome to the tutorial mode! Here you can learn about various Java concepts.");
        System.out.println("1. Variables and Data Types");
        System.out.println("2. Control Flow Statements");
        System.out.println("3. Object-Oriented Programming");
        System.out.println("4. Exception Handling");
        System.out.println("5. Collections Framework");
        System.out.print("Choose a topic (1-5): ");
        int choice = scanner.nextInt();

        switch (choice) {
            case 1:
                explainVariablesAndDataTypes();
                break;
            case 2:
                explainControlFlow();
                break;
            case 3:
                explainOOP();
                break;
            case 4:
                explainExceptionHandling();
                break;
            case 5:
                explainCollections();
                break;
            default:
                System.out.println("Invalid choice. Returning to main menu.");
        }
    }

    private static void explainVariablesAndDataTypes() {
        System.out.println("\n--- Variables and Data Types ---");
        System.out.println("Variables are containers for storing data values.");
        System.out.println("Java has two categories of data types:");
        System.out.println("1. Primitive data types");
        System.out.println("2. Reference/Object data types");
        
        System.out.println("\nPrimitive Data Types:");
        System.out.println("- byte: 8-bit signed two's complement integer");
        System.out.println("- short: 16-bit signed two's complement integer");
        System.out.println("- int: 32-bit signed two's complement integer");
        System.out.println("- long: 64-bit signed two's complement integer");
        System.out.println("- float: single-precision 32-bit IEEE 754 floating point");
        System.out.println("- double: double-precision 64-bit IEEE 754 floating point");
        System.out.println("- boolean: true or false");
        System.out.println("- char: single 16-bit Unicode character");

        System.out.println("\nReference Data Types:");
        System.out.println("- Classes");
        System.out.println("- Interfaces");
        System.out.println("- Arrays");

        System.out.println("\nExample of variable declaration and initialization:");
        System.out.println("int age = 25;");
        System.out.println("String name = \"John Doe\";");
        System.out.println("double salary = 50000.50;");
        System.out.println("boolean isEmployed = true;");
    }

    private static void explainControlFlow() {
        System.out.println("\n--- Control Flow Statements ---");
        System.out.println("Control flow statements regulate the order in which a program's code executes.");
        
        System.out.println("\n1. If-Else Statement:");
        System.out.println("if (condition) {");
        System.out.println("    // code if condition is true");
        System.out.println("} else {");
        System.out.println("    // code if condition is false");
        System.out.println("}");

        System.out.println("\n2. Switch Statement:");
        System.out.println("switch (variable) {");
        System.out.println("    case value1:");
        System.out.println("        // code for value1");
        System.out.println("        break;");
        System.out.println("    case value2:");
        System.out.println("        // code for value2");
        System.out.println("        break;");
        System.out.println("    default:");
        System.out.println("        // default code");
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
    }

    private static void explainOOP() {
        System.out.println("\n--- Object-Oriented Programming (OOP) ---");
        System.out.println("OOP is a programming paradigm based on the concept of 'objects'.");
        System.out.println("The four main principles of OOP are:");

        System.out.println("\n1. Encapsulation:");
        System.out.println("- Bundling of data and methods that operate on that data within a single unit (class)");
        System.out.println("- Achieved through access modifiers (public, private, protected)");

        System.out.println("\n2. Inheritance:");
        System.out.println("- A mechanism where a new class is derived from an existing class");
        System.out.println("- Allows for code reuse and establishes a relationship between parent and child classes");
        System.out.println("Example:");
        System.out.println("class Animal { }");
        System.out.println("class Dog extends Animal { }");

        System.out.println("\n3. Polymorphism:");
        System.out.println("- Ability of objects to take on multiple forms");
        System.out.println("- Achieved through method overloading and method overriding");
        System.out.println("Example of method overriding:");
        System.out.println("class Animal { void makeSound() { } }");
        System.out.println("class Dog extends Animal { void makeSound() { System.out.println(\"Bark\"); } }");

        System.out.println("\n4. Abstraction:");
        System.out.println("- Hiding complex implementation details and showing only essential features");
        System.out.println("- Achieved through abstract classes and interfaces");
        System.out.println("Example:");
        System.out.println("abstract class Shape { abstract double area(); }");
        System.out.println("class Circle extends Shape { double area() { /* implementation */ } }");
    }

    private static void explainExceptionHandling() {
        System.out.println("\n--- Exception Handling ---");
        System.out.println("Exception handling is a mechanism to handle runtime errors.");

        System.out.println("\nTry-Catch Block:");
        System.out.println("try {");
        System.out.println("    // Code that may throw an exception");
        System.out.println("} catch (ExceptionType e) {");
        System.out.println("    // Code to handle the exception");
        System.out.println("} finally {");
        System.out.println("    // Code that always executes");
        System.out.println("}");

        System.out.println("\nTypes of Exceptions:");
        System.out.println("1. Checked Exceptions: Compile-time exceptions (e.g., IOException)");
        System.out.println("2. Unchecked Exceptions: Runtime exceptions (e.g., NullPointerException)");
        System.out.println("3. Error: Serious problems that are not meant to be caught (e.g., OutOfMemoryError)");

        System.out.println("\nThrowing Exceptions:");
        System.out.println("if (someCondition) {");
        System.out.println("    throw new CustomException(\"Error message\");");
        System.out.println("}");

        System.out.println("\nCustom Exceptions:");
        System.out.println("class CustomException extends Exception {");
        System.out.println("    public CustomException(String message) {");
        System.out.println("        super(message);");
        System.out.println("    }");
        System.out.println("}");
    }

    private static void explainCollections() {
        System.out.println("\n--- Collections Framework ---");
        System.out.println("The Collections Framework is a unified architecture for representing and manipulating collections.");

        System.out.println("\nMain interfaces in the Collections Framework:");
        System.out.println("1. List: An ordered collection (e.g., ArrayList, LinkedList)");
        System.out.println("2. Set: A collection that cannot contain duplicate elements (e.g., HashSet, TreeSet)");
        System.out.println("3. Queue: A collection designed for holding elements prior to processing (e.g., PriorityQueue)");
        System.out.println("4. Map: An object that maps keys to values (e.g., HashMap, TreeMap)");

        System.out.println("\nExample usage of ArrayList:");
        System.out.println("List<String> list = new ArrayList<>();");
        System.out.println("list.add(\"Apple\");");
        System.out.println("list.add(\"Banana\");");
        System.out.println("System.out.println(list.get(0)); // Prints: Apple");

        System.out.println("\nExample usage of HashMap:");
        System.out.println("Map<String, Integer> map = new HashMap<>();");
        System.out.println("map.put(\"Apple\", 1);");
        System.out.println("map.put(\"Banana\", 2);");
        System.out.println("System.out.println(map.get(\"Apple\")); // Prints: 1");

        System.out.println("\nIterating through a collection:");
        System.out.println("for (String fruit : list) {");
        System.out.println("    System.out.println(fruit);");
        System.out.println("}");
    }

    private static void practiceJavaExercises() {
        System.out.println("\n=== Java Practice Exercises ===");
        System.out.println("Let's practice some Java programming!");
        
        boolean continuePractice = true;
        while (continuePractice) {
            System.out.println("\nChoose an exercise:");
            System.out.println("1. FizzBuzz");
            System.out.println("2. Palindrome Checker");
            System.out.println("3. Simple Calculator");
            System.out.println("4. Return to Main Menu");
            System.out.print("Enter your choice (1-4): ");
            int choice = scanner.nextInt();
            
            switch (choice) {
                case 1:
                    practiceFizzBuzz();
                    break;
                case 2:
                    practicePalindromeChecker();
                    break;
                case 3:
                    practiceSimpleCalculator();
                    break;
                case 4:
                    continuePractice = false;
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    private static void practiceFizzBuzz() {
        System.out.println("\n--- FizzBuzz Exercise ---");
        System.out.println("Print numbers from 1 to 100. For multiples of 3, print 'Fizz' instead of the number.");
        System.out.println("For multiples of 5, print 'Buzz'. For multiples of both 3 and 5, print 'FizzBuzz'.");
        System.out.println("\nEnter your solution (type 'done' when finished):");
        
        StringBuilder code = new StringBuilder();
        scanner.nextLine(); // Consume newline
        while (true) {
            String line = scanner.nextLine();
            if (line.equals("done")) break;
            code.append(line).append("\n");
        }
        
        System.out.println("\nYour solution:");
        System.out.println(code.toString());
        System.out.println("\nGreat job! Here's a sample solution for comparison:");
        System.out.println("for (int i = 1; i <= 100; i++) {");
        System.out.println("    if (i % 3 == 0 && i % 5 == 0) {");
        System.out.println("        System.out.println(\"FizzBuzz\");");
        System.out.println("    } else if (i % 3 == 0) {");
        System.out.println("        System.out.println(\"Fizz\");");
        System.out.println("    } else if (i % 5 == 0) {");
        System.out.println("        System.out.println(\"Buzz\");");
        System.out.println("    } else {");
        System.out.println("        System.out.println(i);");
        System.out.println("    }");
        System.out.println("}");
    }

    private static void practicePalindromeChecker() {
        System.out.println("\n--- Palindrome Checker Exercise ---");
        System.out.println("Write a method that checks if a given string is a palindrome.");
        System.out.println("A palindrome is a word, phrase, number, or other sequence that reads the same backward as forward.");
        System.out.println("\nEnter your solution (type 'done' when finished):");
        
        StringBuilder code = new StringBuilder();
        scanner.nextLine(); // Consume newline
        while (true) {
            String line = scanner.nextLine();
            if (line.equals("done")) break;
            code.append(line).append("\n");
        }
        
        System.out.println("\nYour solution:");
        System.out.println(code.toString());
        System.out.println("\nGreat attempt! Here's a sample solution for comparison:");
        System.out.println("public static boolean isPalindrome(String str) {");
        System.out.println("    str = str.toLowerCase().replaceAll(\"[^a-zA-Z0-9]\", \"\");");
        System.out.println("    int left = 0;");
        System.out.println("    int right = str.length() - 1;");
        System.out.println("    while (left < right) {");
        System.out.println("        if (str.charAt(left) != str.charAt(right)) {");
        System.out.println("            return false;");
        System.out.println("        }");
        System.out.println("        left++;");
        System.out.println("        right--;");
        System.out.println("    }");
        System.out.println("    return true;");
        System.out.println("}");
    }

    private static void practiceSimpleCalculator() {
        System.out.println("\n--- Simple Calculator Exercise ---");
        System.out.println("Create a simple calculator that can perform addition, subtraction, multiplication, and division.");
        System.out.println("The calculator should take two numbers and an operation as input.");
        System.out.println("\nEnter your solution (type 'done' when finished):");
        
        StringBuilder code = new StringBuilder();
        scanner.nextLine(); // Consume newline
        while (true) {
            String line = scanner.nextLine();
            if (line.equals("done")) break;
            code.append(line).append("\n");
        }
        
        System.out.println("\nYour solution:");
        System.out.println(code.toString());
        System.out.println("\nExcellent work! Here's a sample solution for comparison:");
        System.out.println("public static double calculate(double num1, double num2, char operation) {");
        System.out.println("    switch (operation) {");
        System.out.println("        case '+':");
        System.out.println("            return num1 + num2;");
        System.out.println("        case '-':");
        System.out.println("            return num1 - num2;");
        System.out.println("        case '*':");
        System.out.println("            return num1 * num2;");
        System.out.println("        case '/':");
        System.out.println("            if (num2 != 0) {");
        System.out.println("                return num1 / num2;");
        System.out.println("            } else {");
        System.out.println("                throw new ArithmeticException(\"Division by zero\");");
        System.out.println("            }");
        System.out.println("        default:");
        System.out.println("            throw new IllegalArgumentException(\"Invalid operation\");");
        System.out.println("    }");
        System.out.println("}");
    }
}