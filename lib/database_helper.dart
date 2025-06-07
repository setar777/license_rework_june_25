import 'dart:io';

import 'package:flutter/services.dart';
import 'package:license_rework_june_25/database_selector.dart';
import 'package:license_rework_june_25/models/question_item.dart';
import 'package:license_rework_june_25/services/config_service.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';

class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  factory DatabaseHelper() => _instance;
  static Database? _database;
  DatabaseHelper._internal();

  // Retrieve all ScrapedItems from the database
  Future<List<QuestionItem>> getScrapedItems() async {
    final db = await database;
    // Query the table for all the ScrapedItems.
    final List<Map<String, dynamic>> maps = await db.query(ConfigService().tableName);

    // Convert the List<Map<String, dynamic>> into a List<ScrapedItem>.
    return List.generate(maps.length, (i) {
      return QuestionItem.fromMap(maps[i]);
    });
  }

  Future<Database> get database async {
    if (_database != null) {
      return _database!;
    }
    String? dbToOpen = await _determineDatabaseToOpen();
    if (dbToOpen == null) {
      throw Exception("No suitable database file found to open.");
    }
    _database = await _initDatabase(dbToOpen);
    return _database!;
  }

  Future<String> _getDatabasePath(String dbName) async {
    Directory documentsDirectory = await getApplicationDocumentsDirectory();
    return join(documentsDirectory.path, dbName);
  }

  Future<Database> _initDatabase(String dbName) async {
    String path = await _getDatabasePath(dbName);

    bool dbExists = await File(path).exists();

    if (!dbExists) {
      // If the database doesn't exist on the device, copy it from assets
      print(
        "Database '$dbName' not found on device. Attempting to copy from assets...",
      );
      try {
        ByteData data = await rootBundle.load(
          join("scraper", "databases", dbName),
        );
        List<int> bytes = data.buffer.asUint8List(
          data.offsetInBytes,
          data.lengthInBytes,
        );
        await File(path).writeAsBytes(bytes, flush: true);
        print("Database '$dbName' copied from assets to: $path");
      } catch (e) {
        throw Exception("Failed to copy database '$dbName' from assets: $e");
      }
    } else {
      print("Database '$dbName' already exists at: $path");
    }

    return await openDatabase(path);
  }

  /// Determines which database file to open.
  /// Prioritizes the most recent DB already on the device.
  /// If none found, looks for the most recent DB in assets.
  Future<String?> _determineDatabaseToOpen() async {
    // 1. Check for the most recent database already copied to the device
    String? mostRecentOnDevice =
        await DatabaseSelector.findMostRecentDatabaseInDocuments();
    if (mostRecentOnDevice != null) {
      print("Found most recent database on device: $mostRecentOnDevice");
      return mostRecentOnDevice;
    }

    // 2. If no database is on the device, check for the most recent one in assets
    String? mostRecentInAssets =
        await DatabaseSelector.findMostRecentDatabaseInAssets();
    if (mostRecentInAssets != null) {
      print("Found most recent database in assets: $mostRecentInAssets");
      return mostRecentInAssets;
    }

    // 3. No suitable database found
    print("No database files found either on device or in assets.");
    return null;
  }

  // Method to open a specific database by name (useful if user chooses from a list)
  Future<Database> openSpecificDatabase(String dbName) async {
    _database = await _initDatabase(dbName);
    return _database!;
  }
}
