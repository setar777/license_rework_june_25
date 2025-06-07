// lib/models/scraped_item.dart

class QuestionItem {
  final int? id;
  final String questionUid;
  final String questionText;
  final int pointValue;
  final String answer1Text;
  final String answer2Text;
  final String answer3Text;
  final bool answer1Value;
  final bool answer2Value;
  final bool answer3Value;
  final String hintText;

  QuestionItem({
    this.id,
    required this.questionUid,
    required this.questionText,
    required this.pointValue,
    required this.answer1Text,
    required this.answer2Text,
    required this.answer3Text,
    required this.answer1Value,
    required this.answer2Value,
    required this.answer3Value,
    required this.hintText,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'question_uid': questionUid,
      'question_text': questionText,
      'point_value': pointValue,
      'answer_1_text': answer1Text,
      'answer_2_text': answer2Text,
      'answer_3_text': answer3Text,
      'answer_1_value': answer1Value,
      'answer_2_value': answer2Value,
      'answer_3_value': answer3Value,
      'hint_text': hintText,
    };
  }

  // Convert a Map into a ScrapedItem object. This is useful when reading data from the database.
  factory QuestionItem.fromMap(Map<String, dynamic> map) {
    return QuestionItem(
      id: map['id'],
      questionUid: map['question_uid'] as String,
      questionText: map['question_text'] as String,
      pointValue: map['point_value'] as int,
      answer1Text: map['answer_1_text'] as String,
      answer2Text: map['answer_2_text'] as String,
      answer3Text: map['answer_3_text'] as String,
      answer1Value: (map['answer_1_value'] as int) == 1,
      answer2Value: (map['answer_2_value'] as int) == 1,
      answer3Value: (map['answer_3_value'] as int) == 1,
      hintText: map['hint_text'] as String,
    );
  }

  @override
  String toString() {
    return 'QuestionItem{id: $id, question_uid: $questionUid, question_text: $questionText, point_value: $pointValue, answer_1_text: $answer1Text, answer_2_text: $answer2Text, answer_3_text: $answer3Text, answer_1_value: $answer1Value, answer_2_value: $answer2Value, answer_3_value: $answer3Value, hint_text: $hintText}';
  }

  static QuestionItem example = QuestionItem(
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
  );
}
