package com.ruby.rubyblock;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Mod(RubyBlockMod.MODID)
public class RubyBlockMod {
    public static final String MODID = "rubyblock";
    public static final Logger LOGGER = LoggerFactory.getLogger(RubyBlockMod.class);

    public RubyBlockMod(IEventBus modEventBus) {
        LOGGER.info("Ruby Block Mod loaded!");
    }
}
