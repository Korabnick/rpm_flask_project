$(document).ready(function () {
    var confirmButton = $('#confirmSelection');

    $('#favoriteLocationsModal').on('show.bs.modal', function (event) {
        var modal = $(this);
        $.ajax({
            url: '/get_favorite_locations',
            method: 'GET',
            success: function (response) {
                modal.find('.modal-body ul.list-group').empty();
                response.favoriteLocations.forEach(function (location) {
                    var listItem = $('<li class="list-group-item"></li>');
                    var checkbox = $('<input type="checkbox" class="form-check-input me-2">');
                    var label = $('<label class="form-check-label"></label>').text(location.name);

                    listItem.append(checkbox);
                    listItem.append(label);
                    modal.find('.modal-body ul.list-group').append(listItem);
                });

                confirmButton.prop('disabled', true);
                modal.find('.modal-body ul.list-group input').on('change', function () {
                    var anyChecked = modal.find('.modal-body ul.list-group input:checked').length > 0;
                    confirmButton.prop('disabled', !anyChecked);
                });
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при загрузке избранных локаций:', error);
            }
        });

        confirmButton.on('click', function () {
            var selectedLocations = modal.find('.modal-body ul.list-group input:checked');
            var locationsData = [];

            selectedLocations.each(function (index, checkbox) {
                var locationName = $(checkbox).next().text();
                locationsData.push({
                    name: locationName
                });
            });

            var jsonData = JSON.stringify(locationsData);
            if (jsonData) {
                sessionStorage.setItem('selectedLocations', jsonData);
            }
            modal.modal('hide');
        });
    });

    $('form').on('submit', function () {
        var messageTextarea = $('#message');
        var currentMessage = messageTextarea.val();
        var selectedLocations = sessionStorage.getItem('selectedLocations');
        console.log(selectedLocations);

        if (selectedLocations) {
            // Добавляем данные о локациях только, если они есть
            messageTextarea.val(currentMessage + '\n\nИзбранные локации:\n' + selectedLocations);
        } else {
            // Если нет выбранных локаций, не добавляем блок с избранными локациями
            messageTextarea.val(currentMessage);
        }

        return true;
    });
});
