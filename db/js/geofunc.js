function inPoly(px, py, poly) {
    var angle = 0;
    var p1, p2, p1x, p2x, p1y, p2y;
    for (var i = 0; i < poly.length; i++) {
        p1 = poly[i];
        p2 = poly[(i+1)%n];
        p1x = p1[0];
        p1y = p1[1];
        p2x = p2[0];
        p2y = p2[1];
        angle = angle + calAngle(p1x - px, p1y - py, p2x - px, p2y - py);
    }
    if (Math.abs(angle) < Math.PI) {
        return false;
    }
    return true;
}

function calAngle(x1, y1, x2, y2) {
    var ang1 = Math.atan2(y1, x1);
    var ang2 = Math.atan2(y2, x2);
    var diff_ang = ang1 - ang2;
    if (diff_ang > Math.PI) {
        return 2 * Math.PI - diff_ang;
    } else if (diff_ang < -Math.PI) {
        return diff_ang + 2 * Math;
    }
    return diff_ang;
}

exports.inPoly = inPoly;
