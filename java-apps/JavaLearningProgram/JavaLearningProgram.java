import java.util.Scanner;
import javax.script.ScriptEngineManager;
import javax.script.ScriptEngine;
import javax.script.ScriptException;

public class JavaLearningProgram {
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        System.out.println("Welcome to the Interactive Java Learning Program!");
        
        while (true) {
            System.out.println("\nChoose a topic to learn about:");
            System.out.println("1. Assignment Sequences");
            System.out.println("2. Java Identifiers");
            System.out.println("3. Math Expressions");
            System.out.println("4. Primitive Types");
            System.out.println("5. String Methods");
            System.out.println("6. Exit");
            
            int choice = getIntInput("Enter your choice (1-6): ");
            
            switch (choice) {
                case 1:
                    learnAssignmentSequences();
                    break;
                case 2:
                    learnJavaIdentifiers();
                    break;
                case 3:
                    learnMathExpressions();
                    break;
                case 4:
                    learnPrimitiveTypes();
                    break;
                case 5:
                    learnStringMethods();
                    break;
                case 6:
                    System.out.println("Thank you for using the Java Learning Program. Goodbye!");
                    return;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }
        }
    }

    private static void learnAssignmentSequences() {
        System.out.println("\n--- Assignment Sequences ---");
        System.out.println("Let's trace and evaluate an assignment sequence:");
        
        int a = 5;
        System.out.println("int a = 5;  // a is now " + a);
        
        int b = a + 2;
        System.out.println("int b = a + 2;  // b is now " + b);
        
        a = b * 2;
        System.out.println("a = b * 2;  // a is now " + a);
        
        System.out.println("\nFinal values: a = " + a + ", b = " + b);
        
        int userA = getIntInput("\nNow you try! Enter an initial value for 'a': ");
        System.out.println("int a = " + userA + ";");
        
        int userB = getIntInput("Enter a value to add to 'a' for 'b': ");
        System.out.println("int b = a + " + userB + ";  // b is now " + (userA + userB));
        
        int multiplier = getIntInput("Enter a value to multiply 'b' by for the new 'a': ");
        System.out.println("a = b * " + multiplier + ";  // a is now " + ((userA + userB) * multiplier));
    }

    private static void learnJavaIdentifiers() {
        System.out.println("\n--- Java Identifiers ---");
        System.out.println("Valid Java identifiers must:");
        System.out.println("1. Begin with a letter, underscore (_), or dollar sign ($)");
        System.out.println("2. Contain only letters, digits, underscores, or dollar signs after the first character");
        System.out.println("3. Not be a Java keyword");
        System.out.println("4. Be case-sensitive");
        
        String[] validExamples = {"myVariable", "_count", "$total", "camelCaseIdentifier"};
        String[] invalidExamples = {"123abc", "my-variable", "public"};
        
        System.out.println("\nValid examples:");
        for (String example : validExamples) {
            System.out.println("- " + example);
        }
        
        System.out.println("\nInvalid examples:");
        for (String example : invalidExamples) {
            System.out.println("- " + example);
        }
        
        System.out.println("\nNow you try! Enter an identifier, and I'll tell you if it's valid:");
        String userIdentifier = scanner.nextLine().trim();
        
        if (isValidIdentifier(userIdentifier)) {
            System.out.println("'" + userIdentifier + "' is a valid Java identifier!");
        } else {
            System.out.println("'" + userIdentifier + "' is not a valid Java identifier.");
        }
    }

    private static boolean isValidIdentifier(String identifier) {
        if (identifier.isEmpty()) return false;
        if (!Character.isJavaIdentifierStart(identifier.charAt(0))) return false;
        for (int i = 1; i < identifier.length(); i++) {
            if (!Character.isJavaIdentifierPart(identifier.charAt(i))) return false;
        }
        return !isJavaKeyword(identifier);
    }

    private static boolean isJavaKeyword(String identifier) {
        String[] keywords = {"abstract", "assert", "boolean", "break", "byte", "case", "catch", "char", "class", "const",
                             "continue", "default", "do", "double", "else", "enum", "extends", "final", "finally", "float",
                             "for", "if", "goto", "implements", "import", "instanceof", "int", "interface", "long", "native",
                             "new", "package", "private", "protected", "public", "return", "short", "static", "strictfp", "super",
                             "switch", "synchronized", "this", "throw", "throws", "transient", "try", "void", "volatile", "while"};
        for (String keyword : keywords) {
            if (identifier.equals(keyword)) return true;
        }
        return false;
    }

    private static void learnMathExpressions() {
        System.out.println("\n--- Math Expressions ---");
        System.out.println("Java follows the standard order of operations (PEMDAS).");
        System.out.println("Let's evaluate an expression:");
        
        int result = 10 + 5 * 2 - 8 / 4;
        System.out.println("Expression: 10 + 5 * 2 - 8 / 4");
        System.out.println("Step 1: 5 * 2 = 10");
        System.out.println("Step 2: 8 / 4 = 2");
        System.out.println("Step 3: 10 + 10 - 2 = 18");
        System.out.println("Final result: " + result);
        
        System.out.println("\nNow you try! Enter a math expression using +, -, *, and /:");
        String userExpression = scanner.nextLine().trim();
        
        try {
            double userResult = evaluateExpression(userExpression);
            System.out.println("The result of your expression is: " + userResult);
        } catch (Exception e) {
            System.out.println("Sorry, I couldn't evaluate that expression. Make sure it's valid Java syntax!");
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

    private static void learnPrimitiveTypes() {
        System.out.println("\n--- Primitive Types ---");
        System.out.println("Java has 8 primitive types:");
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
        
        System.out.println("\nLet's practice identifying primitive types by literal value:");
        String[] examples = {"42", "42L", "3.14f", "2.71828", "true", "'A'"};
        for (String example : examples) {
            System.out.print("What type is " + example + "? ");
            String userAnswer = scanner.nextLine().trim().toLowerCase();
            String correctAnswer = getPrimitiveTypeByLiteral(example);
            if (userAnswer.equals(correctAnswer)) {
                System.out.println("Correct!");
            } else {
                System.out.println("Not quite. The correct answer is: " + correctAnswer);
            }
        }
    }

    private static String getPrimitiveTypeByLiteral(String literal) {
        if (literal.endsWith("L") || literal.endsWith("l")) return "long";
        if (literal.endsWith("f") || literal.endsWith("F")) return "float";
        if (literal.contains(".")) return "double";
        if (literal.equals("true") || literal.equals("false")) return "boolean";
        if (literal.startsWith("'") && literal.endsWith("'")) return "char";
        try {
            Integer.parseInt(literal);
            return "int";
        } catch (NumberFormatException e) {
            return "unknown";
        }
    }

    private static void learnStringMethods() {
        System.out.println("\n--- String Methods ---");
        String exampleString = "Hello, World!";
        System.out.println("Let's explore some String methods using the example string: \"" + exampleString + "\"");
        
        System.out.println("\n1. charAt(int index):");
        System.out.println("   exampleString.charAt(1) returns: " + exampleString.charAt(1));
        
        System.out.println("\n2. length():");
        System.out.println("   exampleString.length() returns: " + exampleString.length());
        
        System.out.println("\n3. substring(int beginIndex, int endIndex):");
        System.out.println("   exampleString.substring(7, 12) returns: \"" + exampleString.substring(7, 12) + "\"");
        
        System.out.println("\n4. indexOf(String str):");
        System.out.println("   exampleString.indexOf(\"World\") returns: " + exampleString.indexOf("World"));
        
        System.out.println("\nNow you try! Enter a string:");
        String userString = scanner.nextLine();
        
        System.out.println("\nWhich method would you like to try?");
        System.out.println("1. charAt");
        System.out.println("2. length");
        System.out.println("3. substring");
        System.out.println("4. indexOf");
        
        int choice = getIntInput("Enter your choice (1-4): ");
        
        switch (choice) {
            case 1:
                int index = getIntInput("Enter an index: ");
                try {
                    System.out.println("Result: " + userString.charAt(index));
                } catch (IndexOutOfBoundsException e) {
                    System.out.println("Index out of bounds. Remember, indices start at 0 and go up to length - 1.");
                }
                break;
            case 2:
                System.out.println("Length of your string: " + userString.length());
                break;
            case 3:
                int start = getIntInput("Enter start index: ");
                int end = getIntInput("Enter end index: ");
                try {
                    System.out.println("Result: \"" + userString.substring(start, end) + "\"");
                } catch (IndexOutOfBoundsException e) {
                    System.out.println("Invalid indices. Make sure start < end and both are within the string's length.");
                }
                break;
            case 4:
                System.out.print("Enter a substring to find: ");
                String substr = scanner.nextLine();
                System.out.println("Index of \"" + substr + "\": " + userString.indexOf(substr));
                break;
            default:
                System.out.println("Invalid choice.");
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
}