package com.oldcombat;

import org.bukkit.Bukkit;
import org.bukkit.ChatColor;
import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.scoreboard.*;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;

public class SBPlugin {

    public static void setupScoreboard(Player p) {
        ScoreboardManager m = Bukkit.getScoreboardManager();
        Scoreboard b = m.getNewScoreboard();
        Objective o = b.registerNewObjective("sb", Criteria.DUMMY, 
            ChatColor.GOLD + "" + ChatColor.BOLD + "Jason's Server");
        o.setDisplaySlot(DisplaySlot.SIDEBAR);

        Score s8 = o.getScore(" "); s8.setScore(8); s8.numberFormat(null);
        Score s7 = o.getScore(ChatColor.GRAY + "玩家: " + ChatColor.WHITE + p.getName()); s7.setScore(7); s7.numberFormat(null);
        Score s6 = o.getScore("  "); s6.setScore(6); s6.numberFormat(null);
        Score s5 = o.getScore(ChatColor.GRAY + "延迟: " + (p.getPing() < 100 ? ChatColor.GREEN : ChatColor.RED) + p.getPing() + "ms"); s5.setScore(5); s5.numberFormat(null);
        Score s4 = o.getScore("   "); s4.setScore(4); s4.numberFormat(null);
        Score s3 = o.getScore(ChatColor.GRAY + "在线: " + ChatColor.AQUA + Bukkit.getOnlinePlayers().size() + "人"); s3.setScore(3); s3.numberFormat(null);
        Score s2 = o.getScore("    "); s2.setScore(2); s2.numberFormat(null);
        Score s1 = o.getScore(ChatColor.AQUA + "10.32.134.95:25565"); s1.setScore(1); s1.numberFormat(null);

        p.setScoreboard(b);
    }

    public static void updateAll() {
        for (Player p : Bukkit.getOnlinePlayers()) {
            setupScoreboard(p);
        }
    }
}
