import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class JavaTutorialGUI extends JFrame {
    private CardLayout cardLayout;
    private JPanel mainPanel;
    private int playerHealth = 100;
    private int playerExperience = 0;
    private ArrayList<String> inventory = new ArrayList<>();

    public JavaTutorialGUI() {
        setTitle("Epic Java Adventure: Quest for the Golden Compiler");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(800, 600);
        setLocationRelativeTo(null);

        cardLayout = new CardLayout();
        mainPanel = new JPanel(cardLayout);
        add(mainPanel);

        createWelcomeScreen();
        createMainMenuScreen();
        createBasicLandsScreen();
        // Add more screens here...

        cardLayout.show(mainPanel, "Welcome");
    }

    private void createWelcomeScreen() {
        JPanel welcomePanel = new JPanel(new BorderLayout());
        JLabel welcomeLabel = new JLabel("<html><center>Welcome to the Epic Java Adventure:<br>Quest for the Golden Compiler!</center></html>");
        welcomeLabel.setHorizontalAlignment(JLabel.CENTER);
        welcomePanel.add(welcomeLabel, BorderLayout.CENTER);

        JTextField nameField = new JTextField(20);
        JButton startButton = new JButton("Start Adventure");
        startButton.addActionListener(e -> {
            String playerName = nameField.getText();
            if (!playerName.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Greetings, " + playerName + "! Your quest begins!");
                cardLayout.show(mainPanel, "MainMenu");
            } else {
                JOptionPane.showMessageDialog(this, "Please enter your name, brave programmer!");
            }
        });

        JPanel inputPanel = new JPanel();
        inputPanel.add(new JLabel("Enter your name:"));
        inputPanel.add(nameField);
        inputPanel.add(startButton);
        welcomePanel.add(inputPanel, BorderLayout.SOUTH);

        mainPanel.add(welcomePanel, "Welcome");
    }

    private void createMainMenuScreen() {
        JPanel menuPanel = new JPanel(new GridLayout(0, 1, 10, 10));
        menuPanel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        String[] menuItems = {
            "Explore the Basic Lands",
            "Venture into the OOP Forest",
            "Traverse the Data Structure Mountains",
            "Navigate the Exception Swamp",
            "Enter the Advanced Realm",
            "View Player Status",
            "Learn Java Concepts",
            "Practice Java Exercises",
            "Exit Game"
        };

        for (String item : menuItems) {
            JButton button = new JButton(item);
            button.addActionListener(e -> handleMainMenuChoice(item));
            menuPanel.add(button);
        }

        mainPanel.add(new JScrollPane(menuPanel), "MainMenu");
    }

    private void handleMainMenuChoice(String choice) {
        switch (choice) {
            case "Explore the Basic Lands":
                cardLayout.show(mainPanel, "BasicLands");
                break;
            case "Venture into the OOP Forest":
                // Implement OOP Forest screen
                break;
            case "Traverse the Data Structure Mountains":
                // Implement Data Structure Mountains screen
                break;
            case "Navigate the Exception Swamp":
                // Implement Exception Swamp screen
                break;
            case "Enter the Advanced Realm":
                // Implement Advanced Realm screen
                break;
            case "View Player Status":
                showPlayerStatus();
                break;
            case "Learn Java Concepts":
                // Implement Learn Java Concepts screen
                break;
            case "Practice Java Exercises":
                // Implement Practice Java Exercises screen
                break;
            case "Exit Game":
                System.exit(0);
                break;
        }
    }

    private void createBasicLandsScreen() {
        JPanel basicLandsPanel = new JPanel(new BorderLayout());
        JTextArea storyArea = new JTextArea();
        storyArea.setEditable(false);
        storyArea.setLineWrap(true);
        storyArea.setWrapStyleWord(true);
        storyArea.setText("You enter a serene valley where the fundamentals of Java reside...");

        JPanel challengePanel = new JPanel(new GridLayout(0, 1));
        JButton dataTypesButton = new JButton("Take the Data Types Challenge");
        dataTypesButton.addActionListener(e -> dataTypesChallenge());
        challengePanel.add(dataTypesButton);

        JButton controlFlowButton = new JButton("Face the Control Flow Challenge");
        controlFlowButton.addActionListener(e -> controlFlowChallenge());
        challengePanel.add(controlFlowButton);

        JButton returnButton = new JButton("Return to Main Menu");
        returnButton.addActionListener(e -> cardLayout.show(mainPanel, "MainMenu"));
        challengePanel.add(returnButton);

        basicLandsPanel.add(new JScrollPane(storyArea), BorderLayout.CENTER);
        basicLandsPanel.add(challengePanel, BorderLayout.SOUTH);

        mainPanel.add(basicLandsPanel, "BasicLands");
    }

    private void dataTypesChallenge() {
        String[] dataTypes = {"byte", "short", "int", "long", "float", "double", "boolean", "char"};
        ArrayList<String> remainingTypes = new ArrayList<>(Arrays.asList(dataTypes));
        int correctAnswers = 0;

        for (int i = 0; i < 8; i++) {
            String answer = JOptionPane.showInputDialog(this, "Enter a primitive data type in Java:");
            if (answer != null && remainingTypes.remove(answer.toLowerCase())) {
                JOptionPane.showMessageDialog(this, "Correct! " + explainDataType(answer));
                correctAnswers++;
            } else {
                JOptionPane.showMessageDialog(this, "Incorrect or already mentioned.");
            }
        }

        JOptionPane.showMessageDialog(this, "You correctly named " + correctAnswers + " out of 8 primitive data types.");
        playerExperience += correctAnswers * 5;
    }

    private void controlFlowChallenge() {
        String[] options = {"for", "while", "do-while", "repeat-until"};
        int answer = JOptionPane.showOptionDialog(this,
            "Which of these is NOT a looping structure in Java?",
            "Control Flow Challenge",
            JOptionPane.DEFAULT_OPTION,
            JOptionPane.QUESTION_MESSAGE,
            null,
            options,
            options[0]);

        if (answer == 3) {
            JOptionPane.showMessageDialog(this, "Correct! Java uses for, while, and do-while loops. There is no repeat-until loop in Java.");
            playerExperience += 15;
        } else {
            JOptionPane.showMessageDialog(this, "Incorrect. The correct answer was 'repeat-until'. You take 10 damage.");
            playerHealth -= 10;
        }
    }

    private String explainDataType(String dataType) {
        switch (dataType.toLowerCase()) {
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

    private void showPlayerStatus() {
        JOptionPane.showMessageDialog(this,
            "Health: " + playerHealth + "\n" +
            "Experience: " + playerExperience + "\n" +
            "Inventory: " + inventory,
            "Player Status",
            JOptionPane.INFORMATION_MESSAGE);
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new JavaTutorialGUI().setVisible(true));
    }
}