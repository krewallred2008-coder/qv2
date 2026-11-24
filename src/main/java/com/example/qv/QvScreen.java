package com.example.qv;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.StringWidget;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;

public class QvScreen extends Screen {
    private static final int PAGE_SIZE = 8;

    private enum Tab { WEAPONS, SKINS }

    private record Entry(Component label, Runnable action, boolean active) {
    }

    private Tab tab = Tab.WEAPONS;
    private int page = 0;

    public QvScreen() {
        super(Component.literal("QV"));
    }

    private List<Entry> entries() {
        List<Entry> list = new ArrayList<>();
        if (tab == Tab.WEAPONS) {
            for (String id : QvItems.IDS) {
                list.add(new Entry(Component.translatable("item.qv." + id), () -> give(id), true));
            }
        } else {
            list.add(new Entry(Component.literal("Default skin"), SkinManager::clear, true));
            for (Path p : SkinManager.listSkins()) {
                list.add(new Entry(Component.literal(SkinManager.displayName(p)), () -> SkinManager.apply(p), true));
            }
            if (list.size() == 1) {
                list.add(new Entry(Component.literal("Put .png skins in qv/skins"), () -> { }, false));
            }
        }
        return list;
    }

    private static void give(String id) {
        Minecraft mc = Minecraft.getInstance();
        if (mc.player != null) {
            mc.player.connection.sendCommand("give @s " + QvMod.MOD_ID + ":" + id);
        }
    }

    @Override
    protected void init() {
        int cx = this.width / 2;
        int top = this.height / 2 - 85;

        this.addRenderableWidget(new StringWidget(cx - 100, top - 16, 200, 12,
                Component.literal("QV Menu"), this.font));

        this.addRenderableWidget(Button.builder(
                Component.literal(tab == Tab.WEAPONS ? "> Weapons <" : "Weapons"),
                b -> { tab = Tab.WEAPONS; page = 0; this.rebuildWidgets(); })
                .bounds(cx - 155, top, 100, 20).build());
        this.addRenderableWidget(Button.builder(
                Component.literal(tab == Tab.SKINS ? "> Skins <" : "Skins"),
                b -> { tab = Tab.SKINS; page = 0; this.rebuildWidgets(); })
                .bounds(cx - 50, top, 100, 20).build());
        this.addRenderableWidget(Button.builder(
                Component.literal("Nametags: " + (QvClient.nametagsEnabled ? "ON" : "OFF")),
                b -> { QvClient.toggleNametags(Minecraft.getInstance()); this.rebuildWidgets(); })
                .bounds(cx + 55, top, 100, 20).build());

        List<Entry> all = entries();
        int maxPage = Math.max(0, (all.size() - 1) / PAGE_SIZE);
        page = Math.min(page, maxPage);
        int start = page * PAGE_SIZE;
        for (int i = 0; i < PAGE_SIZE && start + i < all.size(); i++) {
            Entry e = all.get(start + i);
            int col = i % 2;
            int row = i / 2;
            Button b = Button.builder(e.label(), btn -> e.action().run())
                    .bounds(cx - 155 + col * 160, top + 28 + row * 24, 150, 20).build();
            b.active = e.active();
            this.addRenderableWidget(b);
        }

        int navY = top + 28 + 4 * 24 + 6;
        Button prev = Button.builder(Component.literal("< Prev"),
                b -> { page--; this.rebuildWidgets(); }).bounds(cx - 155, navY, 70, 20).build();
        prev.active = page > 0;
        this.addRenderableWidget(prev);
        this.addRenderableWidget(Button.builder(Component.literal("Close"),
                b -> this.onClose()).bounds(cx - 35, navY, 70, 20).build());
        Button next = Button.builder(Component.literal("Next >"),
                b -> { page++; this.rebuildWidgets(); }).bounds(cx + 85, navY, 70, 20).build();
        next.active = page < maxPage;
        this.addRenderableWidget(next);
    }
}
