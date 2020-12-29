import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'Availability.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

class Location extends StatefulWidget {
  @override
  _LocationState createState() => _LocationState();
}

class _LocationState extends State<Location> {
  final _firestore = FirebaseFirestore.instance;
  var mapResult = new Map();

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
      drawer: Drawer(
        child: ListView(
          // Important: Remove any padding from the ListView.
          padding: EdgeInsets.zero,
          children: <Widget>[
            DrawerHeader(
              child: Container(
                child: Align(
                  alignment: Alignment.center,
                  child: Text(
                    'Hey  !',
                    style: GoogleFonts.varela(
                        textStyle: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.bold,
                            letterSpacing: 2,
                            fontSize: 45)),
                  ),
                ),
              ),
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
            ),
            StreamBuilder<QuerySnapshot>(
                stream: _firestore
                    .collection("Peelamedu - Book your Lot")
                    .snapshots(),
                builder: (context, snapshot) {
                  final Result = snapshot.data.docs;
                  for (var i in Result) {
                    mapResult = i.data();
                  }
                  return Column(
                    children: [
                      ListTile(
                        title: Text('USER NAME'),
                        subtitle: Text('${mapResult['UserName']}'),
                      ),
                      ListTile(
                        title: Text('BALANCE'),
                        subtitle: Text('Rs.${mapResult['CurrentBalance']}'),
                        onTap: () {
                          // Update the state of the app.
                          // ...
                        },
                      ),
                      ListTile(
                        title: Text('SMART PARKING MANAGEMENT SYSTEM'),
                        subtitle: Text('By : \n Balaganesh S (19L402)\n Sai Krithik Mulagaletti (18L143) \n Prem Chand S R (19L401)'),

                      ),
                    ],
                  );
                }
                ),
          ],
        ),
      ),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            child: Padding(
              padding: EdgeInsetsDirectional.fromSTEB(15, 15, 15, 0),
              child: Container(
                child: Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    'LOCATION',
                    style: GoogleFonts.varela(
                        textStyle: TextStyle(
                            fontWeight: FontWeight.bold,
                            letterSpacing: 1.5,
                            fontSize: 25)),
                  ),
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(15.0),
            child: TextFormField(
              enabled: false,
              decoration: InputDecoration(
                hintText: ' PEELAMEDU - PSG TECH ',
                filled: true,
                fillColor: Colors.blueGrey[250],
                icon: Icon(
                  Icons.location_on,
                  color: Colors.blue[600],
                ),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.all(Radius.circular(10.0)),
                  borderSide: BorderSide.none,
                ),
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: RaisedButton(
              child: Text(
                'CHECK AVAILABILITY',
                style: GoogleFonts.varela(
                    textStyle: TextStyle(
                        fontWeight: FontWeight.bold,
                        letterSpacing: 1,
                        fontSize: 15)),
              ),
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) {
                      return Availability();
                    },
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
