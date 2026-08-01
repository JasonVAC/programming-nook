package com.oldcombat;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.plugin.java.JavaPlugin;
import org.bukkit.scoreboard.*;

public class ScoreboardPlugin extends JavaPlugin implements Listener {

    @Override
    public void onEnable() {
        getServer().getPluginManager().registerEvents(this, this);
        // Update scoreboard every 20 ticks (1 second)
        getServer().getScheduler().runTaskTimer(this, this::updateScoreboards, 0L, 20L);
        getLogger().info("ScoreboardPlugin loaded!");
    }

    @EventHandler
    public void onJoin(PlayerJoinEvent e) {
        setScoreboard(e.getPlayer());
    }

    public void updateScoreboards() {
        for (Player p : Bukkit.getOnlinePlayers()) {
            setScoreboard(p);
        }
    }

    public void setScoreboard(Player p) {
        ScoreboardManager manager = Bukkit.getScoreboardManager();
        Scoreboard board = manager.getNewScoreboard();
        Objective obj = board.registerNewObjective("side", Criteria.DUMMY, ChatColor.GOLD + "" + ChatColor.BOLD + "✦ My Server ✦");

        obj.setDisplaySlot(DisplaySlot.SIDEBAR);

        // Line 8 - blank
        Score s8 = obj.getScore(" ");
        s8.setScore(8);

        // Line 7 - Player name
        Score s7 = obj.getScore(ChatColor.GRAY + "玩家: " + ChatColor.WHITE + p.getName());
        s7.setScore(7);

        // Line 6 - blank
        Score s6 = obj.getScore("  ");
        s6.setScore(6);

        // Line 5 - Ping
        Score s5 = obj.getScore(ChatColor.GRAY + "延迟: " + ChatColor.GREEN + p.getPing() + "ms");
        s5.setScore(5);

        // Line 4 - blank  
        Score s4 = obj.getScore("   ");
        s4.setScore(4);

        // Line 3 - Online count
        Score s3 = obj.getScore(ChatColor.GRAY + "在线: " + ChatColor.AQUA + Bukkit.getOnlinePlayers().size() + "人");
        s3.setScore(3);

        // Line 2 - blank
        Score s2 = obj.getScore("    ");
        s2.setScore(2);

        // Line 1 - Server version
        Score s1 = obj.getScore(ChatColor.YELLOW + "mc.oldcombat.net");
        s1.setScore(1);

        p.setScoreboard(board);
    }
}
