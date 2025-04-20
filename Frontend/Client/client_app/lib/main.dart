import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'app.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  runApp(MyApp(camera: cameras.first));
}
