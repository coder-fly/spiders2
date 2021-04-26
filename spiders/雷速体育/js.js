const pako = require('pako')
const atob = require('atob');


const roott = function (t, e) {
    for (var i = "", n = 0; n < t.length; n++) {
        var a = t.charCodeAt(n)
            , o = a;
        a >= 65 && a <= 90 && (o = (a - 65 - 1 * e + 26) % 26 + 65),
        a >= 97 && a <= 122 && (o = (a - 97 - 1 * e + 26) % 26 + 97),
            i += String.fromCharCode(o)
    }
    return i
}
const pushmsg = function (t) {
    let e = "";
    e = atob(t);
    const i = e.split("").map(function (t) {
        return t.charCodeAt(0)
    })
    n = new Uint8Array(i)
    a = pako.inflate(n);
    return e = function (t) {
        let e, i, n, a, o = "";
        const r = t.length;
        for (e = 0; e < r;)
            switch ((i = t[e++]) >> 4) {
                case 0:
                case 1:
                case 2:
                case 3:
                case 4:
                case 5:
                case 6:
                case 7:
                    o += String.fromCharCode(i);
                    break;
                case 12:
                case 13:
                    n = t[e++],
                        o += String.fromCharCode((31 & i) << 6 | 63 & n);
                    break;
                case 14:
                    n = t[e++],
                        a = t[e++],
                        o += String.fromCharCode((15 & i) << 12 | (63 & n) << 6 | (63 & a) << 0)
            }
        return o
    }(new Uint16Array(a)),
        unescape(e)
}

function get_data(plaintext){
    return JSON.parse(pushmsg(roott(plaintext, 6)))
}
// console.log(JSON.parse(pushmsg(roott(plaintext, 6))))



