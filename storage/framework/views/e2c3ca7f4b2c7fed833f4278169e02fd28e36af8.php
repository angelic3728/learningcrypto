<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title><?php echo $__env->yieldContent('title'); ?></title>
    <link rel="icon" href="<?php echo e(asset('assets/img/favicon.png')); ?>" type="image/x-icon">
    <link rel="stylesheet" href="<?php echo e(asset('assets/css/style.css')); ?>">
</head>

<body id="dark">
    <div class="vh-100 d-flex justify-content-center">
        <div class="form-access my-auto">
            <?php echo $__env->yieldContent('content'); ?>
        </div>
    </div>
</body><?php /**PATH E:\web\php\learning-crypto\resources\views/layouts/authentication.blade.php ENDPATH**/ ?>