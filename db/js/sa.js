

// map function
function(doc) {
    if (doc.properties.location !== "melbourne") {
        return
    }
    var polymod = require("lib/polygon");
    var geomod = require("lib/geofunc");
    var px = doc.geometry.coordinates[0];
    var py = doc.geometry.coordinates[1];
    var polygons = polymod.polygons;
    var poly;
    for (var i=0; i<polygons.length; i++) {
        poly = polygons[i];
        if (geomod.inPoly(px, py, poly.polygon)) {
            emit(poly.sa2, doc.properties.text);
            return;
        }
    }
}