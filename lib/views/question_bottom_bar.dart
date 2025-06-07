import 'package:flutter/material.dart';
import 'package:license_rework_june_25/services/config_service.dart';
import 'package:license_rework_june_25/views/question_service.dart';

class QuestionBottomBar extends StatefulWidget {
  const QuestionBottomBar({super.key});

  @override
  State<QuestionBottomBar> createState() => _QuestionBottomBarState();
}

class _QuestionBottomBarState extends State<QuestionBottomBar> {
  @override
  Widget build(BuildContext context) {
    return Container(
      color: ConfigService().titleColor,
      child: Row(
        children: [
          Padding(
            padding: EdgeInsets.only(left: 8),
            child: Text(
              "${QuestionService.instance.currentQuestionIndex + 1} / ${QuestionService.instance.numQuestions + 1}",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: ConfigService().onTitleColor,
                fontSize: 15,
              ),
            ),
          ),
          Spacer(),
        ],
      ),
    );
  }
}
