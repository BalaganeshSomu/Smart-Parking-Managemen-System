import 'package:bookyourlot/Location.dart';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class Success extends StatefulWidget {
  @override
  _SuccessState createState() => _SuccessState();
}

class _SuccessState extends State<Success> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AlertDialog(
          title: Text(
            'BOOK YOUR LOT',
            style: GoogleFonts.varela(
              textStyle: TextStyle(
                  color: Colors.blue,
                  letterSpacing: 1.5,
                  fontSize: 20),
            ),
          ),
          content: Text('YOU HAVE SUCCESSFULLY BOOKED A PARKING LOT.YOUR LOT NUMBER WOULD BE DISPLAYED ON THE PARKING ENTRANCE. IF YOU DON\'T SHOW UP BEFORE OUR SLOT ENDS, SLOT GET ALLOCATED TO OTHER USERS. THANK YOU FOR BOOKING WITH US!',
              style: GoogleFonts.varela(
              textStyle: TextStyle(
              color: Colors.black,
              letterSpacing: 1,
              fontSize: 15),
      ),),
          actions: [FlatButton(
            child: Text('OK'),
            onPressed: (){
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) {
                    return Location();
                  },
                ),
              );
            },
          )],
        elevation: 25.0,
      ),
    );

  }
}
