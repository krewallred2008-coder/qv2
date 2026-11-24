package com.example.qv.mixin;

import com.example.qv.QvClient;
import net.minecraft.client.renderer.entity.LivingEntityRenderer;
import net.minecraft.world.entity.LivingEntity;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(LivingEntityRenderer.class)
public abstract class LivingEntityRendererMixin {
    @Inject(method = "shouldShowName", at = @At("HEAD"), cancellable = true, require = 0)
    private void qv$hide(LivingEntity entity, double distance, CallbackInfoReturnable<Boolean> cir) {
        if (!QvClient.nametagsEnabled) {
            cir.setReturnValue(false);
        }
    }
}
