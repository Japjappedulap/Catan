function on_button_click() {
    if (document.getElementById('classic-radio-button').checked) {
        request_new_map('classic');
    }
    if (document.getElementById('extended-radio-button').checked) {
        request_new_map('extended');
    }
}

const fixed_row_1 = 2100;
const fixed_row_2 = 1430;
const fixed_row_3 = 760;
const fixed_row_4 = 90;
const width_augmentation = 1350;
const height_augmentation = 1175;

const dice_width = 450;
const dice_height = 450;

function add_to_classic(position, resource_type, dice) {
    const classic_image_starting_points = [
        [fixed_row_1, 0], // 0
        [fixed_row_1 + width_augmentation, 0], // 1
        [fixed_row_1 + width_augmentation * 2, 0], // 2
        [fixed_row_2, height_augmentation], // 3
        [width_augmentation + fixed_row_2, height_augmentation], // 4
        [2 * width_augmentation + fixed_row_2, height_augmentation], // 5
        [3 * width_augmentation + fixed_row_2, height_augmentation], // 6
        [fixed_row_3, height_augmentation * 2], // 7
        [width_augmentation + fixed_row_3, height_augmentation * 2], // 8
        [2 * width_augmentation + fixed_row_3, height_augmentation * 2], // 9
        [3 * width_augmentation + fixed_row_3, height_augmentation * 2], // 10
        [4 * width_augmentation + fixed_row_3, height_augmentation * 2], // 11
        [fixed_row_2, height_augmentation * 3], // 12
        [width_augmentation + fixed_row_2, height_augmentation * 3], // 13
        [2 * width_augmentation + fixed_row_2, height_augmentation * 3], // 14
        [3 * width_augmentation + fixed_row_2, height_augmentation * 3], // 15
        [fixed_row_1, height_augmentation * 4], // 16
        [fixed_row_1 + width_augmentation, height_augmentation * 4], // 17
        [fixed_row_1 + width_augmentation * 2, height_augmentation * 4], // 18
    ];


    const canvas = document.getElementById('myCanvas');
    const ctx = canvas.getContext('2d');

    let image = document.getElementById(resource_type);
    image.style.width = '50%';
    image.style.height = 'auto';
    // noinspection JSCheckFunctionSignatures
    ctx.drawImage(image, classic_image_starting_points[position][0], classic_image_starting_points[position][1]);

    image = document.getElementById(dice);
    if (image != null) {
        image.style.width = '50%';
        image.style.height = 'auto';
        // noinspection JSCheckFunctionSignatures
        ctx.drawImage(image, classic_image_starting_points[position][0] + dice_width, classic_image_starting_points[position][1] + dice_height);
    }
}

function add_to_extended(position, resource_type, dice) {
    const extended_image_starting_points = [
        [fixed_row_1, 0], // 0
        [fixed_row_1 + width_augmentation, 0], // 1
        [fixed_row_1 + width_augmentation * 2, 0], // 2
        [fixed_row_1 + width_augmentation * 3, 0], // 3

        [fixed_row_2, height_augmentation], // 4
        [width_augmentation + fixed_row_2, height_augmentation], // 5
        [2 * width_augmentation + fixed_row_2, height_augmentation], // 6
        [3 * width_augmentation + fixed_row_2, height_augmentation], // 7
        [4 * width_augmentation + fixed_row_2, height_augmentation], // 8


        [fixed_row_3, height_augmentation * 2], // 9
        [width_augmentation + fixed_row_3, height_augmentation * 2], // 10
        [2 * width_augmentation + fixed_row_3, height_augmentation * 2], // 11
        [3 * width_augmentation + fixed_row_3, height_augmentation * 2], // 12
        [4 * width_augmentation + fixed_row_3, height_augmentation * 2], // 13
        [5 * width_augmentation + fixed_row_3, height_augmentation * 2], // 14

        [fixed_row_4, height_augmentation * 3], // 15
        [width_augmentation + fixed_row_4, height_augmentation * 3], // 16
        [2 * width_augmentation + fixed_row_4, height_augmentation * 3], // 17
        [3 * width_augmentation + fixed_row_4, height_augmentation * 3], // 18
        [4 * width_augmentation + fixed_row_4, height_augmentation * 3], // 19
        [5 * width_augmentation + fixed_row_4, height_augmentation * 3], // 20


        [fixed_row_3, height_augmentation * 4], // 21
        [width_augmentation + fixed_row_3, height_augmentation * 4], // 22
        [2 * width_augmentation + fixed_row_3, height_augmentation * 4], // 23
        [3 * width_augmentation + fixed_row_3, height_augmentation * 4], // 24
        [4 * width_augmentation + fixed_row_3, height_augmentation * 4], // 25

        [fixed_row_2, height_augmentation * 5], // 26
        [fixed_row_2 + width_augmentation, height_augmentation * 5], // 27
        [fixed_row_2 + width_augmentation * 2, height_augmentation * 5], // 28
        [fixed_row_2 + width_augmentation * 3, height_augmentation * 5], // 29
    ];

    const canvas = document.getElementById('myCanvas');
    const ctx = canvas.getContext('2d');

    let image = document.getElementById(resource_type);
    image.style.width = '50%';
    image.style.height = 'auto';
    // noinspection JSCheckFunctionSignatures
    ctx.drawImage(image, extended_image_starting_points[position][0], extended_image_starting_points[position][1]);

    image = document.getElementById(dice);
    if (image != null) {
        image.style.width = '50%';
        image.style.height = 'auto';
        // noinspection JSCheckFunctionSignatures
        ctx.drawImage(image, extended_image_starting_points[position][0] + dice_width, extended_image_starting_points[position][1] + dice_height);
    }
}

function populate_canvas(json_obj) {
    if (json_obj['type'] === 'classic') {
        for (let i = 0; i < 19; ++i) {
            add_to_classic(i, json_obj['tile'][i]['resource_type'], json_obj['tile'][i]['dice']);
        }
    }

    if (json_obj['type'] === 'extended') {
        for (let i = 0; i < 30; ++i) {
            add_to_extended(i, json_obj['tile'][i]['resource_type'], json_obj['tile'][i]['dice']);
        }
    }
}

function request_new_map(map_type) {
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            populate_canvas(JSON.parse(this.responseText));
        }
    };

    xhttp.onloadstart = function () {
        document.getElementById("button").disabled = true;
        const canvas = document.getElementById('myCanvas');
        const context = canvas.getContext('2d');
        context.clearRect(0, 0, canvas.width, canvas.height);
    };

    xhttp.onloadend = function () {
        document.getElementById("button").disabled = false;
    };
    xhttp.open("GET", "catan/" + map_type, true);
    xhttp.send();
}