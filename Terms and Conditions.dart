import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class TermsAndConditions extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Padding(
          padding: const EdgeInsets.all(0.0),
          child: Center(
            child: Text(
              'BOOK YOUR LOT',
              style: GoogleFonts.varela(
                  textStyle: TextStyle(
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2,
                      fontSize: 25)),
            ),
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'TERMS AND CONDITIONS',
              style: GoogleFonts.varela(textStyle: TextStyle(
                color: Colors.blue,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 2,
                  fontSize: 30)),
            ),
            Text(
              '\n 1. No refund will be provided \n 2. No cancellation of spot \n 3. If you don\'t arrive on time,you will have to pay again ',
              style: GoogleFonts.varela(textStyle: TextStyle(
                  letterSpacing: 1,
                  fontSize: 15)),
            ),
          ],
        ),
      ),
    );
  }
}
