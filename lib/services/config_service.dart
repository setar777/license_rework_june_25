// lib/services/config_service.dart

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;
import 'package:license_rework_june_25/hex_color.dart';

class ConfigService {
  static final ConfigService _instance = ConfigService._internal();
  factory ConfigService() => _instance;

  ConfigService._internal();

  Map<String, Map<String, String>>?
  _config; // Nested map: {section: {key: value}}

  // Method to load and parse the .conf file
  Future<void> loadConfig() async {
    if (_config != null) {
      return; // Config already loaded
    }
    try {
      final String response = await rootBundle.loadString('config.conf');
      _config = _parseConfString(response);
      print("Configuration loaded successfully.");
    } catch (e) {
      print("Error loading config.conf: $e");
      // Handle error, e.g., throw an exception or set default values
      _config = {}; // Fallback to an empty map to avoid null issues
    }
  }

  // Parses the INI-like .conf string into a nested map
  Map<String, Map<String, String>> _parseConfString(String confString) {
    final Map<String, Map<String, String>> parsedConfig = {};
    String? currentSection;

    for (String line in confString.split('\n')) {
      final String trimmedLine = line.trim();

      if (trimmedLine.isEmpty ||
          trimmedLine.startsWith('#') ||
          trimmedLine.startsWith(';')) {
        continue; // Skip empty lines and comments
      }

      // Check for section header: [section_name]
      final RegExp sectionRegex = RegExp(r'^\[(.*?)\]$');
      final Match? sectionMatch = sectionRegex.firstMatch(trimmedLine);
      if (sectionMatch != null) {
        currentSection = sectionMatch.group(1)?.trim();
        if (currentSection != null) {
          parsedConfig[currentSection] = {}; // Initialize the section map
        }
        continue;
      }

      // Check for key=value pair
      if (currentSection != null && trimmedLine.contains('=')) {
        final int equalsIndex = trimmedLine.indexOf('=');
        final String key = trimmedLine.substring(0, equalsIndex).trim();
        final String value = trimmedLine.substring(equalsIndex + 1).trim();
        parsedConfig[currentSection]![key] = value;
      }
    }
    return parsedConfig;
  }

  // Generic getter for config values by section and key
  String? getValue(String section, String key) {
    if (_config == null) {
      throw StateError("Config not loaded. Call loadConfig() first.");
    }
    return _config?[section]?[key];
  }

  // Specific getters for common config values
  String get tableName => getValue('database', 'tableName') ?? 'scraped_items';
  Color get backgroundColor =>
      HexColor.fromHex(getValue('color', 'background') ?? '#ff0000');
  Color get titleColor =>
      HexColor.fromHex(getValue('color', 'title') ?? '#ff0000');
  Color get onTitleColor =>
      HexColor.fromHex(getValue('color', 'onTitle') ?? '#ffffff');
  Color get textOnTitleColor =>
      HexColor.fromHex(getValue('color', 'textOnTitle') ?? '#ffffff');
  Color get textOnBackgroundColor =>
      HexColor.fromHex(getValue('color', 'textOnBackground') ?? '#ffffff');

  bool get isLoaded => _config != null;
}
