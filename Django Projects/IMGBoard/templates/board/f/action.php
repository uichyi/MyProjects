<?php

print_r($_POST);

$errors = [];
$data = [];

if (empty($_POST['body'])) {
    $errors['body'] = 'Body is required.';
}

if (!empty($errors)) {
    $data['success'] = false;
    $data['errors'] = $errors;
} else {
    $data['success'] = true;
    $data['message'] = 'Success!';
}

echo json_encode($data);