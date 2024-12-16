# The-Odd-Spark
'The Odd Spark': Building a Game Powered by Flutter and Gemini-2.0 flash AI Feedback:
Overview
This blog outlines the creation of The Odd Spark, a fun and interactive game that challenges users to identify the "odd one out" from a series of options. The game is implemented using Flutter for the frontend, BigQuery for the dataset, and Gemini 2.0 for generating dynamic AI-driven feedback.


# Key Features
#Dynamic Gameplay: The game fetches its data from Google BigQuery using a Google Cloud Function, ensuring real-time data updates.


#Time-Based Challenges: Players have 10 seconds to select the odd one out, adding an element of urgency and excitement.

#AI-Driven Feedback: The game integrates Google's Gemini-2.0-flash-exp model to provide interactive and motivational feedback through Zappy, the Lightning Fox.


#Engaging User Interface: The game features a visually appealing design, incorporating Zappy's SVG image, a pixel-style font, and a modern, user-friendly interface.


# Tech Stack Used:

# Flutter: 
Utilized to construct the frontend UI and manage the interactive gameplay with smooth animations and a responsive design.

# Firebase Hosting: 

Provides a reliable and scalable platform to host the web version of the game, ensuring quick and global access for players.

# Google BigQuery: 
Serves as the central repository for storing and retrieving game data, enabling efficient handling of large datasets for seamless gameplay.

# Google Cloud Functions: 
Powers the backend logic and acts as a middleware layer to fetch data from BigQuery, ensuring secure and scalable interactions.

# Gemini-2.0-flash-exp: 
Employed for generating personalized, engaging AI feedback for players, adding an interactive and motivational element to the game.

# SVG Assets: 
Enhances the visual appeal with scalable and vibrant graphics, like Zappy the Lightning Fox, to elevate the overall user experience.

# Step-by-Step Implementation

# Setting Up the Backend
   
The backend is crucial for retrieving the game data from BigQuery. This is facilitated through a Cloud Function, ensuring data is fetched in real-time.
BigQuery:

The Cloud Function efficiently connects the game to BigQuery, enabling dynamic updates and scaling of the dataset as needed:
Future<void> fetchGameData() async {
  final response = await http.get(Uri.parse(
      'https://us-central1-my-project-s7s1.cloudfunctions.net/bigquery-game-backend-v2'));
  if (response.statusCode == 200) {
    setState(() {
      gameData = jsonDecode(response.body)['gameData'];
      startTimer();
    });
  } else {
    setState(() {
      message = "Failed to load game data.";
    });
  }
}

The Cloud Function connects the game to BigQuery, allowing you to update or scale the dataset as needed.

# The Frontend: Flutter UI
   
The game's UI is crafted using Flutter, featuring a contrasting black background, vibrant buttons, and a cheerful SVG of Zappy the Lightning Fox. Here's a glimpse of the main screen setup:
return Scaffold(
  backgroundColor: backgroundColor,
  appBar: AppBar(
    title: Center(
      child: Text(
        'The Odd Spark',
        style: TextStyle(
          fontFamily: 'PixelifySans',
          fontSize: 24,
          color: Colors.white,
        ),
      ),
    ),
    backgroundColor: Colors.transparent,
    elevation: 0,
  ),
  body: Center(
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SvgPicture.asset(characterSvg, height: 150, width: 150),
        Text('$characterName - $characterTrait',
          style: TextStyle(fontSize: 18, color: Colors.white),
        ),
        ...
      ],
    ),
  ),
);

# Adding Zappy: The Lightning Fox

Zappy is central to "The Odd Spark," providing dynamic feedback to the user. The handleSelection method demonstrates how Zappy responds to user actions:
void handleSelection(String selectedItem) async {
  timer.cancel();
  final correctAnswer = gameData[currentIndex]['oddOneOut'];
  if (selectedItem == correctAnswer) {
    setState(() {
      score++;
      message = "Correct! Your current score is $score.";
    });
    final response = await fetchGeminiResponse("Encourage a player who scored $score points.");
    if (response.isNotEmpty) {
      // Process response to generate Zappy's message
    }
  } else {
    setState(() {
      message = "Oops, That's Wrong! Your score is still $score.";
    });
    final response = await fetchGeminiResponse("Encourage a player who got the wrong answer.");
    if (response.isNotEmpty) {
      // Process response for Zappy
    }
  }
  Future.delayed(Duration(seconds: 2), moveToNextSet);
}


# AI Feedback with Gemini

The game leverages the Gemini API to deliver personalized, AI-driven feedback based on player performance. The following code demonstrates how the feedback is fetched:
Future<Map<String, dynamic>> fetchGeminiResponse(String prompt) async {
  const String geminiUrl =
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent";
  const String apiKey = "<API_KEY>";
  try {
    final response = await http.post(
      Uri.parse(geminiUrl),
      headers: {
        "Content-Type": "application/json",
        "x-goog-api-key": apiKey,
      },
      body: jsonEncode({"contents": [{"parts": [{"text": prompt}]}]}),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    return {};
  } catch (e) {
    return {};
  }
}

The AI feedback is presented in Zappy's voice, enhancing the game's interactivity and engagement.

# Final Score Page
At the end of each game, players receive a summary of their score and final feedback from Zappy.
class FinalScorePage extends StatelessWidget {
  final int score;
  final int total;
  final String aiFeedback;
  FinalScorePage({required this.score, required this.total, required this.aiFeedback});
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(...),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Game Over!', style: TextStyle(fontSize: 30, color: Colors.white)),
            Text('Your final score is $score out of $total.',
                style: TextStyle(fontSize: 24, color: Colors.white)),
            Text(aiFeedback, style: TextStyle(fontSize: 18, fontStyle: FontStyle.italic)),
            ElevatedButton(...),
          ],
        ),
      ),
    );
  }
}

# Firebase Hosting:

Deployment is straightforward with Firebase Hosting. The game is deployed to the web with these simple steps :
flutter clean
flutter pub get
flutter build web
firebase deploy
Hosting URL generatedThe Odd Spark - Game:


# Full Demo link: https://youtu.be/-6BqbR6NbOo?si=r5FYmnCsMFoIMePa
# GitHub: https://github.com/RaaghaviNithiyanandan/The-Odd-Spark

# Future Developments:
Here are 4 key features and enhancements to focus, prioritizing impact and feasibility:

1.Difficulty Levels & Dynamic Adjustment:

Implement Easy, Medium, and Hard difficulty settings. These would adjust parameters like the time limit, complexity of the items, and the number of choices per set.

2. Dynamic Data generation through AI:
   
Create a wide variety of data sets, either through variations of specific categories or by generating entirely random sets through AI.

3. Category-Based Game Mode:
   
Allow players to choose categories for the game (e.g., animals, foods, objects, shapes, etc.). This would make the game more educational and engaging.

4. User Progress Tracking and Basic Leaderboard:

Track user scores, best times, and the number of games played. Store this data locally on the device (or cloud for later).

# Conclusion

"The Odd Spark" is more than just a game - it's an engaging experience enhanced by AI. By combining Flutter's capabilities, BigQuery's scalability, and Gemini's intelligence, this project showcases how cutting-edge technologies can be used to create captivating user experiences.
 
