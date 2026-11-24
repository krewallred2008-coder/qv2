package com.example.qv;

import java.util.ArrayList;
import java.util.List;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.item.Item;

public final class QvItems {
    public static final String[] IDS = { "sidearm", "heavy_pistol", "revolver", "machine_pistol", "smg", "shotgun", "assault_rifle", "carbine", "battle_rifle", "bolt_sniper", "heavy_sniper", "auto_sniper", "marksman_rifle", "combat_knife", "curved_knife", "butterfly_knife", "dagger", "tanto", "machete" };
    public static final List<Item> ALL = new ArrayList<>();

    public static void register() {
        for (String name : IDS) {
            Identifier id = Identifier.fromNamespaceAndPath(QvMod.MOD_ID, name);
            ResourceKey<Item> key = ResourceKey.create(Registries.ITEM, id);
            Item item = new Item(new Item.Properties().setId(key).stacksTo(1));
            Registry.register(BuiltInRegistries.ITEM, key, item);
            ALL.add(item);
        }
    }
}
