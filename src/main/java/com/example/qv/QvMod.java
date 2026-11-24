package com.example.qv;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.creativetab.v1.CreativeModeTabEvents;
import net.minecraft.world.item.CreativeModeTabs;

public class QvMod implements ModInitializer {
    public static final String MOD_ID = "qv";

    @Override
    public void onInitialize() {
        QvItems.register();
        CreativeModeTabEvents.modifyOutputEvent(CreativeModeTabs.COMBAT)
                .register(output -> QvItems.ALL.forEach(item -> output.accept(item)));
    }
}
