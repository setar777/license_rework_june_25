import 'package:flutter/material.dart';
import 'package:license_rework_june_25/services/config_service.dart';
import 'package:license_rework_june_25/views/question_service.dart';

class QuestionBody extends StatefulWidget {
  const QuestionBody({super.key});

  @override
  State<QuestionBody> createState() => _QuestionBodyState();
}

class _QuestionBodyState extends State<QuestionBody> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: double.infinity,
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              QuestionService.instance.currentQuestion.questionText,
              style: TextStyle(
                fontWeight: FontWeight.w800,
                color: ConfigService().textOnBackgroundColor,
                fontSize: 21,
              ),
            ),
            LayoutBuilder(
              builder: (context, constraints) {
                return IntrinsicHeight(
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Image.asset(
                        "assets/example.jpg",
                        width: constraints.maxWidth * 0.45,
                      ),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.max,
                          mainAxisAlignment: MainAxisAlignment.spaceAround,
                          children: [
                            Row(
                              children: [
                                Image.asset("assets/btn_optquestion_1.gif"),
                                Padding(
                                  padding: const EdgeInsets.only(left: 14),
                                  child: Text(
                                    QuestionService
                                        .instance
                                        .currentQuestion
                                        .answer1Text,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color:
                                          ConfigService().textOnBackgroundColor,
                                      fontSize: 18,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            Row(
                              children: [
                                Image.asset("assets/btn_optquestion_1.gif"),
                                Padding(
                                  padding: const EdgeInsets.only(left: 14),
                                  child: Text(
                                    QuestionService
                                        .instance
                                        .currentQuestion
                                        .answer2Text,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color:
                                          ConfigService().textOnBackgroundColor,
                                      fontSize: 18,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            Row(
                              children: [
                                Image.asset("assets/btn_optquestion_1.gif"),
                                Padding(
                                  padding: const EdgeInsets.only(left: 14),
                                  child: Text(
                                    QuestionService
                                        .instance
                                        .currentQuestion
                                        .answer3Text,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color:
                                          ConfigService().textOnBackgroundColor,
                                      fontSize: 18,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                );
              },
            ),
            /*
            Container(
              color: Colors.red,
              child: LayoutBuilder(
                builder:
                    (context, constraints) => Row(
                      children: [
                        Image.asset(
                          "assets/example.jpg",
                          width: constraints.maxWidth * 0.45,
                        ),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            LayoutBuilder(
                              builder: (context, answerConstraints) {
                                print(answerConstraints);
                                print(constraints);
                                return SizedBox(
                                  width: double.infinity,
                                  child: Row(
                                    children: [
                                      Image.asset(
                                        "assets/btn_optquestion_1.gif",
                                      ),
                                      Padding(
                                        padding: const EdgeInsets.only(
                                          left: 14,
                                        ),
                                        child: Text(
                                          widget.question.answer1Text,
                                          style: TextStyle(
                                            fontWeight: FontWeight.w800,
                                            color:
                                                ConfigService()
                                                    .textOnBackgroundColor,
                                            fontSize: 18,
                                          ),
                                        ),
                                      ),
                                    ],
                                  ),
                                );
                              },
                            ),
                            Row(
                              children: [
                                Image.asset("assets/btn_optquestion_1.gif"),
                                Padding(
                                  padding: const EdgeInsets.only(left: 14),
                                  child: Text(
                                    widget.question.answer2Text,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color:
                                          ConfigService().textOnBackgroundColor,
                                      fontSize: 18,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                            Row(
                              children: [
                                Image.asset("assets/btn_optquestion_1.gif"),
                                Padding(
                                  padding: const EdgeInsets.only(left: 14),
                                  child: Text(
                                    widget.question.answer3Text,
                                    style: TextStyle(
                                      fontWeight: FontWeight.w800,
                                      color:
                                          ConfigService().textOnBackgroundColor,
                                      fontSize: 18,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ],
                    ),
              ),
            ),
          */
          ],
        ),
      ),
    );
  }
}
