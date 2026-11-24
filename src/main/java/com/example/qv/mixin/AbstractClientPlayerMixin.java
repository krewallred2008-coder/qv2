package com.example.qv.mixin;

import com.example.qv.SkinManager;
import net.minecraft.client.Minecraft;
import net.minecraft.client.player.AbstractClientPlayer;
import net.minecraft.world.entity.player.PlayerSkin;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

@Mixin(AbstractClientPlayer.class)
public abstract class AbstractClientPlayerMixin {
    @Inject(method = "getSkin", at = @At("RETURN"), cancellable = true, require = 0)
    private void qv$skin(CallbackInfoReturnable<PlayerSkin> cir) {
        if ((Object) this == Minecraft.getInstance().player) {
            cir.setReturnValue(SkinManager.override(cir.getReturnValue()));
        }
    }
}
