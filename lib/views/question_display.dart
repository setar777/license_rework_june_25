import 'package:flutter/material.dart';
import 'package:license_rework_june_25/models/question_item.dart';
import 'package:license_rework_june_25/services/config_service.dart';
import 'package:license_rework_june_25/views/question_title_bar.dart';

class QuestionDisplay extends StatefulWidget {
  const QuestionDisplay({super.key});

  @override
  State<QuestionDisplay> createState() => _QuestionDisplayState();
}

class _QuestionDisplayState extends State<QuestionDisplay> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Container(
          color: ConfigService().backgroundColor,
          child: Column(
            children: [
              QuestionTitleBar(
                question: QuestionItem(
                  questionUid: "1.1.01-110",
                  questionText: "Wie wirkt sich Müdigkeit beim Fahren aus?",
                  pointValue: 4,
                  answer1Text: "Nachlassende Aufmerksamkeit",
                  answer2Text: "Verzögerte Reaktionen",
                  answer3Text: "Eingeschränkte Wahrnehmung",
                  answer1Value: true,
                  answer2Value: true,
                  answer3Value: true,
                  hintText:
                      "Müdigkeit kann den Fahrer auf vielfältige Art und W\n\n...\n\nIn der Vollversion finden Sie die vollständige Erklärung und ggf. die StVO Paragraphen zu dieser Frage.",
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
