<?php $__env->startSection('title'); ?>
Login
<?php $__env->stopSection(); ?>
<?php $__env->startSection('content'); ?>
<form method="POST" action="<?php echo e(route('login')); ?>">
    <?php echo csrf_field(); ?>
    <span>Sign In</span>
    <!-- Email Address -->
    <div class="form-group">
        <input id="email" class="form-control block mt-1 w-full" type="email" name="email" :value="old('email')" placeholder="Email Address" required autofocus />
    </div>

    <!-- Password -->
    <div class="form-group">
        <input id="password" class="form-control block mt-1 w-full" type="password" name="password" required autocomplete="current-password" placeholder="Password" />
    </div>

    <!-- Remember Me -->
    <div class="custom-control custom-checkbox">
        <input type="checkbox" class="custom-control-input" id="form-checkbox">
        <label class="custom-control-label" for="form-checkbox">Remember me</label>
    </div>

    <div class="flex items-center justify-end mt-2">
        <?php if(Route::has('password.request')): ?>
        <a class="underline text-sm text-gray-600 hover:text-gray-900" href="<?php echo e(route('password.request')); ?>">
            <?php echo e(__('Forgot your password?')); ?>

        </a>
        <?php endif; ?>
        <button type="submit" class="btn btn-primary">Sign In</button>
    </div>
</form>
<div class="flex items-center justify-end mt-4">
    <h2>Don't have an account?
        <a class="underline text-sm text-gray-600 hover:text-gray-900" href="<?php echo e(route('register')); ?>">
            <?php echo e(__('Sign Up here')); ?>

        </a>
    </h2>
</div>
<?php $__env->stopSection(); ?>
<?php echo $__env->make('layouts.authentication', \Illuminate\Support\Arr::except(get_defined_vars(), ['__data', '__path']))->render(); ?><?php /**PATH E:\web\php\learning-crypto\resources\views/auth/login.blade.php ENDPATH**/ ?>