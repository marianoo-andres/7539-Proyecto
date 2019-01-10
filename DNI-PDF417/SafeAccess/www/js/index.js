/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

// implement your decoding as you need it, this just does ASCII decoding
function hex2a(hex) {
    var str = '';
    for (var i = 0; i < hex.length; i += 2) {
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    }
    return str;
}

var app = {
    // Application Constructor
    initialize: function() {
        this.bindEvents();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },

    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicity call 'app.receivedEvent(...);'
    onDeviceReady: function() {
        app.receivedEvent('deviceready');
        
        var resultDiv = document.getElementById('resultDiv');
        var ipInputElement = document.getElementById('ipInput');
        var ip = ipInputElement.value;
        
        /**
         * Scan these barcode types
         * Available: "PDF417", "USDL", "QR Code", "Code 128", "Code 39", "EAN 13", "EAN 8", "ITF", "UPCA", "UPCE", "Aztec", "Data Matrix"
         */
        var types = ["PDF417"];

        /**
         * Initiate scan with options
         * NOTE: Some features are unavailable without a license
         * Obtain your key at http://pdf417.mobi
         */
        var options = {
            beep : true,  // Beep on
            noDialog : true, // Skip confirm dialog after scan
            uncertain : false, //Recommended
            quietZone : false, //Recommended
            highRes : false, //Recommended
            inverseScanning: false,
            frontFace : false
        };

        // Note that each platform requires its own license key

        // This license key allows setting overlay views for this application ID: mobi.pdf417.demo
        // Valid until 2018-12-10
        var licenseiOs = "sRwAAAEYbWFyaWFub2FuZHJlcy5zYWZlYWNjZXNzrjdMYB/oEfN3jp8gpwc9jTy0Nd7UKyHMPn9VIgpIKoCY68m9nLbOk1VT/rODi7CkFR+q4XaM02l9GXztYkKqmCN4VgkCEkVid7jB5+Bgpq3uriHMAXQB4eiqY/cmSIZ1AaPZQw==";

        // This license is only valid for package name "mobi.pdf417.demo"
        var licenseAndroid = "sRwAAAAQbW9iaS5wZGY0MTcuZGVtb2uCzTSwE5Pixw1pJDqrv3T8G8jLYsNmfW+d4cayaSCjwfRtJzKqVtPhAW9bx9lGvg/VldZCWtWc+gjT/4yTY/+BDqQxT6zmNT8qRt324hvuB2FU8mimuh/otPy/fqpwtG8hxXk=";

        scanButton.addEventListener('click', function() {
            ip = ipInputElement.value;
            console.log(ip);  
            cordova.plugins.pdf417Scanner.scan(
            
                // Register the callback handler
                function callback(scanningResult) {
                    
                    // handle cancelled scanning
                    if (scanningResult.cancelled == true) {
                        resultDiv.innerHTML = "Cancelled!";
                        return;
                    }
                    // Obtain list of recognizer results
                    var recognizerResult = scanningResult.resultList[0];
                    var data = recognizerResult.data;
                    var dataHtml = "Data: " + recognizerResult.data + "<br>"
                    console.log(data);
                    resultDiv.innerHTML = dataHtml;

                    //var xhr   = new XMLHttpRequest();   // new HttpRequest instance
                    //var url  = "http://127.0.0.1:5000/"; 
                    //xhr.open("GET", "https://www.google.com/");
                    //xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
                    //var jsonData = {"data":data};
                    //xhr.onload = function () {
                      //console.log("xhr.responseText:" + xhr.responseText);
                      //console.log("xhr.readyState :" + xhr.readyState );
                      //console.log("xhr.response :" + xhr.response);
                      //console.log("xhr.responseType:" + xhr.responseType);
                      //console.log("xhr.responseURL:" + xhr.responseURL);
                      //console.log("xhr.responseXML:" + xhr.responseXML);
                      //console.log("xhr.status:" + xhr.status);
                      //console.log("xhr.statusText:" + xhr.statusText);
                    //}
                    //xhr.send(JSON.stringify(jsonData));
                    //xhr.send();
                   const options = {
 						method: 'post',
  						data: { "data": data}
					};
                    cordova.plugin.http.setDataSerializer('json');
                    cordova.plugin.http.sendRequest('http://'+ip+':5000/', options, function(response) {
                      // prints 200
                      console.log(response.status);
                      console.log(response.data);
                    }, function(response) {
                      // prints 403
                      console.log(response.status);
                     
                      //prints Permission denied
                      console.log(response.error);
                    });
                },
                
                // Register the error callback
                function errorHandler(err) {
                    alert('Error: ' + err);
                },

                types, options, licenseiOs, licenseAndroid
            );
        });

    },
    // Update DOM on a Received Event
    receivedEvent: function(id) {
        console.log('Received Event: ' + id);
    }
};
