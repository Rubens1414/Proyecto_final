import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'screens/home_page.dart';
import 'screens/camera_screen.dart';
import 'screens/instructions.dart';

class MyApp extends StatelessWidget {
  final CameraDescription camera;

  const MyApp({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: '/',
      routes: {
        '/': (context) => HomePage(camera: camera),
        '/camera': (context) => CameraScreen(camera: camera),
        '/instructions': (context) => InstructionsScreen(),
      },
    );
  }
}
