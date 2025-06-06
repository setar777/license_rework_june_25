import 'package:flutter/material.dart';
import 'package:license_rework_june_25/services/config_service.dart';
import 'package:license_rework_june_25/views/question_service.dart';

class QuestionTitleBar extends StatelessWidget {
  const QuestionTitleBar({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: ConfigService().titleColor,
      child: Row(
        children: [
          Container(
            color: ConfigService().onTitleColor,
            child: Padding(
              padding: const EdgeInsets.all(6),
              child: Icon(
                Icons.info_outline,
                color: ConfigService().textOnTitleColor,
              ),
            ),
          ),
          Padding(
            padding: EdgeInsets.only(left: 8),
            child: Text(
              QuestionService.instance.currentQuestion.questionUid,
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: ConfigService().onTitleColor,
                fontSize: 15,
              ),
            ),
          ),
          Spacer(),
          Container(
            color: ConfigService().onTitleColor,
            child: Padding(
              padding: const EdgeInsets.all(6),
              child: Icon(Icons.lightbulb_outlined, color: Colors.red),
            ),
          ),
          Spacer(),
          Padding(
            padding: EdgeInsets.only(right: 8),
            child: Text(
              "Punkte: ${QuestionService.instance.currentQuestion.pointValue}",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                color: ConfigService().onTitleColor,
                fontSize: 15,
              ),
            ),
          ),
          Container(
            color: ConfigService().onTitleColor,
            child: Padding(
              padding: const EdgeInsets.all(6),
              child: Icon(Icons.close, color: ConfigService().textOnTitleColor),
            ),
          ),
        ],
      ),
    );
  }
}
