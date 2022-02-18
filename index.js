import * as crypto from 'crypto';

export class Security {
    static consumerId = "bdf33b06-d562-420a-bc31-2831d11a8016";
    static publicKey = `-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvj75/rCN0TWGde+4NUpi
    BIRRYetxXj8prEFmncGISyw/vBNQDcxJi7tmy7ZpkPYr5lDSMxpTqpylRUrRf796
    d3Aeam1P1oAoQdruJNAjfHMCCowA8Xi7YG5JR2dZm3DipO48hxbNvV/xhjK7jcyf
    OQut1FF+5B937otUqy+eEQBu5oXZZvsieV8MxofiiBq9F0Bl0rEdlOQ7XmTdSs6u
    spsOVi/yZrJ2hlGnthLq79G7HcZUCNBeW9/UkLTKEBbe+n6dBt2su9hEz7CBbqIy
    oiKi9RU6GjhT2FIogP9YfnqrHZHC5pCbL85jkwty1opEW45SFfLsWasOUP0lXS52
    1QIDAQAB
    -----END PUBLIC KEY-----`
    static privateKey = `-----BEGIN PRIVATE KEY-----
MIIEwAIBADANBgkqhkiG9w0BAQEFAASCBKowggSmAgEAAoIBAQC+Pvn+sI3RNYZ1
77g1SmIEhFFh63FePymsQWadwYhLLD+8E1ANzEmLu2bLtmmQ9ivmUNIzGlOqnKVF
StF/v3p3cB5qbU/WgChB2u4k0CN8cwIKjADxeLtgbklHZ1mbcOKk7jyHFs29X/GG
MruNzJ85C63UUX7kH3fui1SrL54RAG7mhdlm+yJ5XwzGh+KIGr0XQGXSsR2U5Dte
ZN1Kzq6ymw5WL/JmsnaGUae2Eurv0bsdxlQI0F5b39SQtMoQFt76fp0G3ay72ETP
sIFuojKiIqL1FToaOFPYUiiA/1h+eqsdkcLmkJsvzmOTC3LWikRbjlIV8uxZqw5Q
/SVdLnbVAgMBAAECggEBALPCw+uhHc+xuMSVZ0SLbUSBVnikxLFeE11dSr4DkWoe
fHaU9Q6kmlW7FK2mReegg+iTM5rv5GCQtSVdRclkvy4+Na8wbMDsxZ08ZctJFE7S
SPp4QafpAXxjmUAr6qKSrsVTCsRGis7G6mt4YnnhAA4h9/Vnr/OTvHodEzrRupSq
ZtYIlPHRL3vFoInmxuMqO1OuUMkw/PgnqBf5oliwoaAGaKKVaa5it7qgyIUm32bp
T3+kJ0cDzO5oS7aHylow8NhdHS42Ih2YySyf+JAP1NXYk2szFn9ZW7eZamMqCk1f
ZCgvwG91kDpt5/thf5XKjHZqyGXR40Pa33in0GKyOMECgYEA7lIFBU1Fr34FKKG/
Cos02naTYlV++WihwN27L0xXJKvMjZ3XZDQ/UtA1FzbzIfSAF/JoupVz+5lOzE6g
GV0brzoF/oT1dy+YiaIW2IbdzDrQ6Dgbr6d7T1fsn79UDTKn5Tcf2m39koJNKTqa
qNvKLhIsv+tPcXSjPV9maUlEKiUCgYEAzFv39pKN5ti4SmFZ2IV7WFYZb1s072wK
hOv//ijrX5vTdPAp1vxe7o8FrYWazah/taDIKJlebZ+Xd+xX0KSUxiNwqbz/ZUbA
i2D07ANRorMl64VMteYyx4VGM9IGlYRUHMMYX/CF+L23yYSsOV+7WCI36s5WPDx1
67Fem1NsgvECgYEA2OqYnUnHCsO2aFRIcY1hLxNMdO2Co/qDd+uaC6P9kWg5yBCJ
0y/nDzZpjFa8mARWbvV6M5ICvle9LCLIgC2KHETA3fghADm3Klb5Wl3vFYvXR/aB
5LCZgQ9zVbetBlI8FVrGSGdirO6i0sr/qIBdFu/+ATVp2seiKSNjMKO6Qm0CgYEA
mBHX8yQbdCzQ9oh60ySBJLrtMnAsc/1x1nfHhtnsTLkoIVyVxeUGv36uOvGwwFki
r4V1bMC0A98+V38H2bqe+tJkg+qgIj0ECrObjgTqOqgVD62h57nlD5OdKfKf86ME
9GI5QSs6hl6m5M5VWlxijLLp6VCh2zEijsDuJadumAECgYEA2H92CMFYwmGOjI7r
YqjNQT5QjdG8ZwYdfMAR/DGeTJ+LNy5xuErsr+emdlT6QJ+2xjtIUMA8Xr/UgX3E
q1mhwtlvvhCQod9Kvv+pioyxZzmDjdpWTsLc6iZ+2cXHow/Mel/nNEW4mcr6InK5
ZJwzZrpeplt8HUWFBIw7v5BEywI=
-----END PRIVATE KEY-----`
    static keyVersion = 1;

    static async generateSecurityHeaders() {
        if(!this.consumerId || !this.publicKey || !this.privateKey || !this.keyVersion) {
            throw new Error(`Couldn't create security headers. Missing environment configuration.`);
        }

        const headers = {
            'WM_SEC.KEY_VERSION': this.keyVersion,
            'WM_CONSUMER.ID': this.consumerId,
            'WM_CONSUMER.INTIMESTAMP': Date.now().toString()
        };

        headers['WM_SEC.AUTH_SIGNATURE'] = this.createSignature(headers);

        return headers;
    }

     static createSignature(headers) {
        const signer = crypto.createSign('RSA-SHA256');

        const payload = this.generateSignatureMap(headers);
        console.log('PAYLOAD', payload)
        signer.update(payload);
        signer.end();

        return signer.sign(this.privateKey, 'base64');
    }

    // Can be used to double-check signature.
    verifySignature(signature, headers) {
        const verifier = crypto.createVerify('RSA-SHA256');

        const payload = this.generateSignatureMap(headers);

        verifier.update(payload);

        return verifier.verify(this.publicKey, signature, 'base64');
    }

     static generateSignatureMap(headers) {
        let keys = Object.keys(headers).sort();
        let vals = [];

        for(let k of keys) {
            vals.push(headers[k].toString().trim());
        }

        return vals.join('\n') + '\n';
    }
}

console.log(Security.generateSecurityHeaders())