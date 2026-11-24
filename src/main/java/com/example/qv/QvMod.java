package com.example.qv;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.world.item.CreativeModeTabs;

public class QvMod implements ModInitializer {
    public static final String MOD_ID = "qv";

    @Override
    public void onInitialize() {
        QvItems.register();
        ItemGroupEvents.modifyEntriesEvent(CreativeModeTabs.COMBAT)
                .register(entries -> QvItems.ALL.forEach(entries::accept));
    }
}
