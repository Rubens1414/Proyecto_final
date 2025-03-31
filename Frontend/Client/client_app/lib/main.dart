import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'dart:io';


void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  final cameras = await availableCameras();
  runApp(MyApp(camera: cameras.first));
}

class MyApp extends StatelessWidget {
  final CameraDescription camera;
  const MyApp({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: CameraScreen(camera: camera),
    );
  }
}

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;
  const CameraScreen({Key? key, required this.camera}) : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(widget.camera, ResolutionPreset.medium);
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _captureAndSendImage() async {
    try {
      await _initializeControllerFuture;
      final image = await _controller.takePicture();
      final bytes = await File(image.path).readAsBytes();
      String base64Image = base64Encode(bytes);

      final response = await http.post(
        Uri.parse('http://10.0.2.2:8000/predict'), 
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'image': base64Image}),
      );


      if (response.statusCode == 200) {
        print('Respuesta del servidor: ${response.body}');
      } else {
        print('Error en la respuesta del servidor');
      }
    } catch (e) {
      print('Error al capturar o enviar la imagen: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: GestureDetector(
        onTap: _captureAndSendImage, 
        child: FutureBuilder<void>(
          future: _initializeControllerFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              return CameraPreview(_controller);
            } else {
              return const Center(child: CircularProgressIndicator());
            }
          },
        ),
      ),
    );
  }
}
