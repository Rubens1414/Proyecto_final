import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

class HomePage extends StatelessWidget {
  final CameraDescription camera;

  const HomePage({Key? key, required this.camera}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    const Color appBarColor = Color(0xFF0D47A1); // Azul oscuro
    const Color buttonColor = Color(0xFF64B5F6); // Azul claro
    const Color textColor = Colors.white; // Contraste alto

    return Scaffold(
      appBar: AppBar(
        title: const Text('App para personas con discapacidad visual'),
        centerTitle: true,
        backgroundColor: appBarColor,
        foregroundColor: textColor,
      ),
      body: Column(
        children: [
          Expanded(
            child: SizedBox.expand(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.camera_alt, size: 32),
                  label: const Text(
                    'Acceder a cámara con IA',
                    style: TextStyle(fontSize: 24),
                  ),
                  onPressed: () {
                    Navigator.pushNamed(context, '/camera');
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: buttonColor,
                    foregroundColor: textColor,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            child: SizedBox.expand(
              child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: ElevatedButton.icon(
                  icon: const Icon(Icons.info_outline, size: 32),
                  label: const Text(
                    'Instrucciones',
                    style: TextStyle(fontSize: 24),
                  ),
                  onPressed: () {
                    Navigator.pushNamed(context, '/instructions');
                  },
                  style: ElevatedButton.styleFrom(
                    backgroundColor: buttonColor,
                    foregroundColor: textColor,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
