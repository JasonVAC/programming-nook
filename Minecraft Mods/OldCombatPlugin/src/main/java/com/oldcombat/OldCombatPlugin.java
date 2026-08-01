package com.oldcombat;

import org.bukkit.Bukkit;
import org.bukkit.attribute.Attribute;
import org.bukkit.attribute.AttributeInstance;
// Paper 1.21.8: use ATTACK_SPEED, ENTITY_INTERACTION_RANGE (no GENERIC_/PLAYER_ prefix)
import org.bukkit.configuration.file.FileConfiguration;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.EntityDamageByEntityEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.java.JavaPlugin;

public final class OldCombatPlugin extends JavaPlugin implements Listener {

    @Override
    public void onEnable() {
        saveDefaultConfig();
        getServer().getPluginManager().registerEvents(this, this);

        // Start scoreboard updater (every 20 ticks = 1 second)
        getServer().getScheduler().runTaskTimer(this, SBPlugin::updateAll, 0L, 20L);

        getLogger().info("OldCombat loaded! 1.8 combat is back!");
    }

    @Override
    public void onDisable() {
        getLogger().info("OldCombat disabled.");
    }

    @EventHandler
    public void onPlayerJoin(PlayerJoinEvent event) {
        Player player = event.getPlayer();
        FileConfiguration config = getConfig();

        // Set up scoreboard
        SBPlugin.setupScoreboard(player);

        if (config.getBoolean("combat.enableInstantAttack", true)) {
            AttributeInstance speedAttr = player.getAttribute(Attribute.ATTACK_SPEED);
            if (speedAttr != null) {
                speedAttr.setBaseValue(config.getDouble("combat.attackSpeed", 1000.0));
            }

            AttributeInstance reachAttr = player.getAttribute(Attribute.ENTITY_INTERACTION_RANGE);
            if (reachAttr != null) {
                reachAttr.setBaseValue(config.getDouble("combat.attackReach", 4.5));
            }
        }
    }

    @EventHandler
    public void onHit(EntityDamageByEntityEvent event) {
        if (event.getDamager() instanceof Player) {
            FileConfiguration config = getConfig();
            if (config.getBoolean("combat.enableInstantAttack", true)) {
                double multiplier = config.getDouble("combat.damageMultiplier", 1.0);
                if (multiplier != 1.0) {
                    event.setDamage(event.getDamage() * multiplier);
                }
            }
        }
    }
}
