function onFileUpload(fileSelector, alertSelector, optionsRowSelector) {
    $(alertSelector).hide();

    $(fileSelector).on('change', function() {
        var fileName = $(this).val().split('\\').pop();
        $(this).siblings('label').addClass('selected').html(fileName);

        $(optionsRowSelector).removeClass('d-none');

        $(alertSelector).html(
            'You uploaded <kbd class="ml-1">'
            + fileName
            + '</kbd> <button class="close" data-dismiss="alert">×</button>');
        $(alertSelector).show();
    });
}


function showSpinnerOnButton(spinnerSelector, buttonSelector) {
    $(buttonSelector).click(function(){
        $(spinnerSelector).removeClass('d-none');
    });
}


function enableCountrySelect(countrySelector) {
    $(countrySelector).countrySelect({
        defaultCountry: 'gb',
        preferredCountries: ['ro', 'gb'],
        responsiveDropdown: false
      });
}

