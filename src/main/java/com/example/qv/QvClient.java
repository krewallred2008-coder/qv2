package com.example.qv;

import com.mojang.blaze3d.platform.InputConstants;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.keymapping.v1.KeyMappingHelper;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import org.lwjgl.glfw.GLFW;

public class QvClient implements ClientModInitializer {
    public static boolean nametagsEnabled = true;

    private static KeyMapping nametagKey;
    private static KeyMapping menuKey;

    @Override
    public void onInitializeClient() {
        KeyMapping.Category category = KeyMapping.Category.register(
                Identifier.fromNamespaceAndPath(QvMod.MOD_ID, "main"));

        nametagKey = KeyMappingHelper.registerKeyMapping(new KeyMapping(
                "key.qv.nametags", InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_N, category));
        menuKey = KeyMappingHelper.registerKeyMapping(new KeyMapping(
                "key.qv.menu", InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_F9, category));

        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            while (nametagKey.consumeClick()) {
                toggleNametags(client);
            }
            while (menuKey.consumeClick()) {
                client.setScreen(new QvScreen());
            }
        });
    }

    public static void toggleNametags(Minecraft client) {
        nametagsEnabled = !nametagsEnabled;
        if (client.player != null) {
            client.player.displayClientMessage(
                    Component.literal("Nametags: " + (nametagsEnabled ? "ON" : "OFF")), true);
        }
    }
}
