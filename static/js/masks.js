document.addEventListener('DOMContentLoaded', function () {

    /*
    =========================================
    CPF
    =========================================
    */

    document.querySelectorAll('.cpf-mask').forEach(el => {

        IMask(el, {
            mask: '000.000.000-00'
        });

    });


    /*
    =========================================
    CNPJ
    =========================================
    */

    document.querySelectorAll('.cnpj-mask').forEach(el => {

        IMask(el, {
            mask: '00.000.000/0000-00'
        });

    });


    /*
    =========================================
    TELEFONE
    =========================================
    */

    document.querySelectorAll('.phone-mask').forEach(el => {

        IMask(el, {
            mask: [
                {
                    mask: '(00) 0000-0000'
                },
                {
                    mask: '(00) 00000-0000'
                }
            ]
        });

    });


    /*
    =========================================
    CEP
    =========================================
    */

    document.querySelectorAll('.cep-mask').forEach(el => {

        IMask(el, {
            mask: '00000-000'
        });

    });


    /*
    =========================================
    PLACA
    =========================================
    */

    document.querySelectorAll('.placa-mask').forEach(el => {

        IMask(el, {
            mask: 'aaa-0000',
            prepare: str => str.toUpperCase()
        });

    });


    /*
    =========================================
    DINHEIRO
    =========================================
    */

    document.querySelectorAll('.money-mask').forEach(el => {

        IMask(el, {

            mask: Number,

            scale: 2,

            signed: false,

            thousandsSeparator: '.',

            padFractionalZeros: true,

            normalizeZeros: true,

            radix: ',',

            mapToRadix: ['.']

        });

    });

});