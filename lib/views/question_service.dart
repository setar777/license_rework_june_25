import 'package:license_rework_june_25/models/question_item.dart';

class QuestionService {
  QuestionService._privateConstructor();
  static final QuestionService _instance =
      QuestionService._privateConstructor();
  static QuestionService get instance => _instance;

  final List<QuestionItem> _questions = [];
  final int _index = 0;

  QuestionItem get currentQuestion =>
      _index > _questions.length - 1
          ? QuestionItem.example
          : _questions[_index];
  int get numQuestions => _questions.length;
  int get currentQuestionIndex => _index;
}
