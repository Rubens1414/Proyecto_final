import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'dart:io';
import 'dart:convert';
import '../services/api_service.dart';
import '../services/tts_service.dart';

class CameraScreen extends StatefulWidget {
  final CameraDescription camera;
  const CameraScreen({Key? key, required this.camera}) : super(key: key);

  @override
  _CameraScreenState createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;
  String _interpretation = "Presiona la pantalla para analizar la escena.";
  final TTSService _ttsService = TTSService();

  @override
  void initState() {
    super.initState();
    _controller = CameraController(widget.camera, ResolutionPreset.medium);
    _initializeControllerFuture = _controller.initialize();

    // Leer instrucciones al iniciar la pantalla
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _speakInstructions();
    });
  }

  void _speakInstructions() {
    const String instructionText =
        "Bienvenido a la cámara. Toca la pantalla para que la aplicación tome una foto y la analice mediante inteligencia artificial.";
    _ttsService.speak(instructionText);
  }

  @override
  void dispose() {
    _controller.dispose();
    _ttsService.stop();
    super.dispose();
  }

  Future<void> _captureAndSendImage() async {
    try {
      await _initializeControllerFuture;
      final image = await _controller.takePicture();
      final bytes = await File(image.path).readAsBytes();
      String base64Image = base64Encode(bytes);

      bool success = await APIService.sendImage(base64Image);
      if (success) {
        await _fetchInterpretation();
      }
    } catch (e) {
      print('Error al capturar o enviar la imagen: $e');
    }
  }

  Future<void> _fetchInterpretation() async {
    final interpretation = await APIService.fetchInterpretation();
    if (interpretation != null) {
      setState(() {
        _interpretation = interpretation;
      });
      await _ttsService.speak(interpretation);
    }
  }

  @override
  Widget build(BuildContext context) {
    const Color appBarColor = Color(0xFF0D47A1); // Azul oscuro
    const Color textColor = Colors.white; // Contraste alto

    return Scaffold(
      appBar: AppBar(
        title: const Text('Cámara'),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        backgroundColor: appBarColor,
        foregroundColor: textColor,
      ),
      body: GestureDetector(
        onTap: _captureAndSendImage,
        child: FutureBuilder<void>(
          future: _initializeControllerFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              return Stack(
                children: [
                  // Contenedor con borde de 5px alrededor de la cámara
                  Padding(
                    padding: const EdgeInsets.all(5.0),
                    child: Container(
                      decoration: BoxDecoration(
                        border: Border.all(color: Colors.blueAccent, width: 2),
                        borderRadius: BorderRadius.circular(5),
                      ),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(5),
                        child: CameraPreview(_controller),
                      ),
                    ),
                  ),
                  Align(
                    alignment: Alignment.bottomCenter,
                    child: Container(
                      padding: const EdgeInsets.all(16),
                      color: Colors.black54,
                      child: Text(
                        _interpretation,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                        ),
                        textAlign: TextAlign.center,
                      ),
                    ),
                  ),
                ],
              );
            } else {
              return const Center(child: CircularProgressIndicator());
            }
          },
        ),
      ),
    );
  }
}
