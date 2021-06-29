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


function toggleCountrySelect(toggleOnSelector, toggleOffSelector, countrySelector) {
    $(toggleOnSelector).on('click', function (e) {
      $(countrySelector).prop('disabled', false);
    });
    $(toggleOffSelector).on('click', function (e) {
      $(countrySelector).prop('disabled', true);
    });
}


function enableCarousel() {
    $('#method_carousel').on('slide.bs.carousel', function (e) {
        document.getElementById("carousel_index").value = e.to;
      })
}


function switchAccordionSigns(accordionSelector, switchIconSelector) {
    $(accordionSelector).on('hide.bs.collapse', function (e) {
        $(switchIconSelector).html('<i class="fas fa-plus"></i>');
      });
    $(accordionSelector).on('show.bs.collapse', function (e) {
        $(switchIconSelector).html('<i class="fas fa-minus"></i>');
    });
}

