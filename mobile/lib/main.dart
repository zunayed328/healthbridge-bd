import 'package:flutter/material.dart';

void main() {
  runApp(const HealthBridgeApp());
}

class HealthBridgeApp extends StatelessWidget {
  const HealthBridgeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'HealthBridge BD',
      home: const Scaffold(
        body: Center(
          child: Text('HealthBridge BD'),
        ),
      ),
    );
  }
}
