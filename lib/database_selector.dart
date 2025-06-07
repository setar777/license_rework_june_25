import 'dart:convert';
import 'dart:io';

import 'package:flutter/services.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

class DatabaseSelector {
  // Method to find the most recent database in the application documents directory

  static Future<String?> findMostRecentDatabaseInDocuments() async {
    Directory documentsDirectory = await getApplicationDocumentsDirectory();
    String dbDirectoryPath = documentsDirectory.path;

    DateTime? latestTimestamp;
    String? mostRecentDbName;

    try {
      final dir = Directory(dbDirectoryPath);
      if (await dir.exists()) {
        await for (FileSystemEntity entity in dir.list()) {
          if (entity is File && entity.path.endsWith('.db')) {
            String fileName = p.basename(
              entity.path,
            ); // e.g., data_1717523999.123456.db

            // Regular expression to extract the timestamp part
            RegExp regExp = RegExp(r'data_(\d+\.?\d*)\.db');
            Match? match = regExp.firstMatch(fileName);

            if (match != null && match.groupCount > 0) {
              String timestampStr =
                  match.group(1)!; // e.g., "1717523999.123456"

              try {
                // Convert to double (seconds since epoch)
                double secondsSinceEpoch = double.parse(timestampStr);

                // Convert to milliseconds since epoch for Dart's DateTime
                int millisecondsSinceEpoch = (secondsSinceEpoch * 1000).toInt();

                DateTime currentDbTime = DateTime.fromMillisecondsSinceEpoch(
                  millisecondsSinceEpoch,
                );

                if (latestTimestamp == null ||
                    currentDbTime.isAfter(latestTimestamp)) {
                  latestTimestamp = currentDbTime;
                  mostRecentDbName = fileName;
                }
              } catch (e) {
                print("Error parsing timestamp from $fileName: $e");
              }
            }
          }
        }
      }
    } catch (e) {
      print("Error listing databases in documents directory: $e");
    }
    return mostRecentDbName;
  }

  // Method to find the most recent database in your assets (bundled with the app)
  static Future<String?> findMostRecentDatabaseInAssets() async {
    final manifestContent = await rootBundle.loadString('AssetManifest.json');
    final Map<String, dynamic> manifest = json.decode(manifestContent);

    DateTime? latestTimestamp;
    String? mostRecentDbName;

    final dbPaths =
        manifest.keys
            .where(
              (String key) =>
                  key.startsWith('scraper/databases/') && key.endsWith('.db'),
            )
            .toList();

    for (String path in dbPaths) {
      String fileName = p.basename(path); // e.g., data_1717523999.123456.db

      RegExp regExp = RegExp(r'data_(\d+\.?\d*)\.db');
      Match? match = regExp.firstMatch(fileName);

      if (match != null && match.groupCount > 0) {
        String timestampStr = match.group(1)!;

        try {
          double secondsSinceEpoch = double.parse(timestampStr);
          int millisecondsSinceEpoch = (secondsSinceEpoch * 1000).toInt();
          DateTime currentDbTime = DateTime.fromMillisecondsSinceEpoch(
            millisecondsSinceEpoch,
          );

          if (latestTimestamp == null ||
              currentDbTime.isAfter(latestTimestamp)) {
            latestTimestamp = currentDbTime;
            mostRecentDbName = fileName;
          }
        } catch (e) {
          print("Error parsing timestamp from $fileName: $e");
        }
      }
    }
    return mostRecentDbName;
  }
}
