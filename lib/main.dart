import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:license_rework_june_25/database_helper.dart';
import 'package:license_rework_june_25/services/config_service.dart';
import 'package:license_rework_june_25/views/question_display.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:sqflite_common_ffi_web/sqflite_ffi_web.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  if (kIsWeb) {
    // Change default factory for web
    databaseFactory = databaseFactoryFfiWeb;
  } else if (Platform.isWindows || Platform.isLinux || Platform.isMacOS) {
    // Initialize FFI for desktop platforms
    sqfliteFfiInit();
    // Change the default factory for sqflite to use FFI
    databaseFactory = databaseFactoryFfi;
  }

  final configService = ConfigService();
  await configService.loadConfig();

  final dbHelper = DatabaseHelper();
  try {
    await dbHelper.database;
    print("Database opened successfully after discovery!");
  } catch (e) {
    print("Error opening database: $e");
  }

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
      ),
      home: const QuestionDisplay(),
    );
  }
}
