import 'package:flutter/material.dart';
import 'package:license_rework_june_25/services/config_service.dart';
import 'package:license_rework_june_25/views/question_body.dart';
import 'package:license_rework_june_25/views/question_bottom_bar.dart';
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
        child: LayoutBuilder(
          builder: (context, constraints) {
            return Container(
              color: ConfigService().backgroundColor,
              width: constraints.maxWidth,
              height: constraints.maxHeight,
              // color: ConfigService().backgroundColor,
              child: Column(
                children: [
                  QuestionTitleBar(),

                  Expanded(flex: 3, child: QuestionBody()),
                  Expanded(flex: 1, child: Container()),
                  QuestionBottomBar(),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
