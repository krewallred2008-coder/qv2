package com.example.qv;

import com.mojang.blaze3d.platform.NativeImage;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.stream.Stream;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.core.ClientAsset;
import net.minecraft.resources.Identifier;
import net.minecraft.world.entity.player.PlayerSkin;

/** Loads PNG skins from <game dir>/qv/skins and swaps the local player's skin (client-side only). */
public final class SkinManager {
    private static Identifier current;

    public static Path skinDir() {
        Path dir = FabricLoader.getInstance().getGameDir().resolve("qv").resolve("skins");
        try {
            Files.createDirectories(dir);
        } catch (IOException ignored) {
        }
        return dir;
    }

    public static List<Path> listSkins() {
        List<Path> out = new ArrayList<>();
        try (Stream<Path> s = Files.list(skinDir())) {
            s.filter(p -> p.getFileName().toString().toLowerCase(Locale.ROOT).endsWith(".png"))
                    .sorted().forEach(out::add);
        } catch (IOException ignored) {
        }
        return out;
    }

    public static String displayName(Path p) {
        String n = p.getFileName().toString();
        return n.substring(0, n.length() - 4);
    }

    public static void apply(Path png) {
        try (InputStream in = Files.newInputStream(png)) {
            NativeImage image = NativeImage.read(in);
            String safe = displayName(png).toLowerCase(Locale.ROOT).replaceAll("[^a-z0-9_.-]", "_");
            Identifier id = Identifier.fromNamespaceAndPath(QvMod.MOD_ID, "skin/" + safe);
            Minecraft.getInstance().getTextureManager().register(id, new DynamicTexture(() -> "qv skin", image));
            current = id;
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void clear() {
        current = null;
    }

    public static PlayerSkin override(PlayerSkin original) {
        if (current == null) {
            return original;
        }
        return new PlayerSkin(new ClientAsset.ResourceTexture(current, current),
                original.cape(), original.elytra(), original.model(), original.secure());
    }

    private SkinManager() {
    }
}
