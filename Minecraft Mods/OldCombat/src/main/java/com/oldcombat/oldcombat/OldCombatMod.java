package com.oldcombat.oldcombat;

import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.common.ModConfigSpec;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.player.Player;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Mod(OldCombatMod.MODID)
public class OldCombatMod {
    public static final String MODID = "oldcombat";
    public static final Logger LOGGER = LoggerFactory.getLogger(OldCombatMod.class);

    // Config values
    private static ModConfigSpec.Builder BUILDER = new ModConfigSpec.Builder();
    public static final ModConfigSpec.BooleanValue ENABLE_INSTANT_ATTACK;
    public static final ModConfigSpec.DoubleValue ATTACK_SPEED_VALUE;
    public static final ModConfigSpec.DoubleValue ATTACK_REACH;
    public static final ModConfigSpec.DoubleValue ATTACK_DAMAGE_BONUS;
    public static final ModConfigSpec SPEC;

    static {
        BUILDER.push("combat");

        ENABLE_INSTANT_ATTACK = BUILDER
                .comment("Remove attack cooldown (1.8-style instant attacks)")
                .define("enableInstantAttack", true);

        ATTACK_SPEED_VALUE = BUILDER
                .comment("Attack speed value (default 1000 = no cooldown)")
                .defineInRange("attackSpeed", 1000.0, 4.0, 100000.0);

        ATTACK_REACH = BUILDER
                .comment("Player attack reach in blocks (default 4.5)")
                .defineInRange("attackReach", 4.5, 1.0, 10.0);

        ATTACK_DAMAGE_BONUS = BUILDER
                .comment("Additional damage multiplier (1.0 = normal)")
                .defineInRange("damageMultiplier", 1.0, 0.1, 100.0);

        BUILDER.pop();
        SPEC = BUILDER.build();
    }

    public OldCombatMod(IEventBus modEventBus, ModContainer container) {
        container.registerConfig(ModConfig.Type.SERVER, SPEC);
        NeoForge.EVENT_BUS.register(this);
        LOGGER.info("Old Combat Mod loaded! Get ready for 1.8 combat!");
    }

    @SubscribeEvent
    public void onPlayerJoin(EntityJoinLevelEvent event) {
        if (event.getEntity() instanceof Player player && event.getLevel().isClientSide() == false) {
            if (ENABLE_INSTANT_ATTACK.get()) {
                AttributeInstance speedAttr = player.getAttribute(Attributes.ATTACK_SPEED);
                if (speedAttr != null) {
                    // Set base value to huge number so cooldown is effectively zero
                    speedAttr.setBaseValue(ATTACK_SPEED_VALUE.get());
                }

                AttributeInstance reachAttr = player.getAttribute(Attributes.ENTITY_INTERACTION_RANGE);
                if (reachAttr != null) {
                    reachAttr.setBaseValue(ATTACK_REACH.get());
                }
            }
        }
    }

    @SubscribeEvent
    public void onHurt(LivingDamageEvent.Pre event) {
        // Apply damage multiplier if the damage source is from a player
        if (event.getSource().getEntity() instanceof Player) {
            double multiplier = ATTACK_DAMAGE_BONUS.get();
            if (multiplier != 1.0) {
                event.setNewDamage(event.getNewDamage() * (float) multiplier);
            }
        }
    }
}
